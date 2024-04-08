from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    get_jwt_identity,
    unset_jwt_cookies,
    jwt_required,
    JWTManager,
    create_refresh_token,
    current_user,
)
from flask_restful import Resource, Api, fields, marshal_with

from ..api import api_response, api_abort
from server.db.models import (
    Company,
    Employee,
    Chat,
    Message,
    MessageFile,
    User,
    ChatMember,
    MessageStatus,
    PinnedMessages
)

from flask import abort, request

from werkzeug.exceptions import Conflict, Forbidden
import logging
from datetime import datetime, timedelta

from .helpers import is_current_user_company_employee, is_current_user_in_chat, is_company_employee


class LiveChatResource(Resource):
    @jwt_required()
    def get(self, chat_id):

        chat_member = is_current_user_in_chat(chat_id)
        if not chat_member:
            raise Forbidden

        # get all messages for the chat member other then the one they sent
        # if we sent a message it will be delivered automatically for the sender
        target_msgs = MessageStatus.get_all_not_delivered_messages(
            employee_id=chat_member.employee_id
        )
        return api_response(
            target_msgs,
            "Messages Received",
        )

    @jwt_required()
    def put(self, chat_id):

        chat_member = is_current_user_in_chat(chat_id)
        if not chat_member:
            raise Forbidden

        data = request.get_json()
        message_ids = data.get("message_ids")

        updated_ids = []
        for msg_id in message_ids:
            if not Message.query.filter_by(id=msg_id, chat_id=chat_id).first():
                continue
            message_status = MessageStatus.query.filter_by(
                employee_id=chat_member.employee_id, message_id=msg_id
            ).first()
            message_status.is_delivered = True
            message_status.update()
            updated_ids.append(msg_id)

        return api_response(updated_ids, "Messages ids updated")


class ChatGroupCreateResource(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()

        company_id = data.get("company_id")
        employee = is_current_user_company_employee(company_id)
        if not employee:
            raise Forbidden

        participants = data.get("participants")
        if not participants:
            return api_abort(
                400, "Can't create an empty group, atleast a participant needed"
            )
        name = data.get("name")
        avatar = data.get("avatar")

        if not all((company_id, name)):
            abort(400, "Some required fields missing")

        new_chat = Chat(
            company_id=company_id,
            is_group=True,
            name=name,
            owner_id=employee.id,
            avatar=avatar,
        )
        new_chat.insert()

        # there might be a better way of doing this
        new_member = ChatMember(chat_id=new_chat.id, employee_id=employee.id)
        new_member.insert()
        for participant in participants:
            # check if the participants are from the company
            if employee.id == participant:
                continue
            if not is_company_employee(company_id=company_id, employee_id=participant):
                continue
            new_member = ChatMember(chat_id=new_chat.id, employee_id=participant)
            new_member.insert()

        return api_response(new_chat.get_all(employee_id=employee.id), "Group chat created")


class GetChatInfoResource(Resource):
    @jwt_required()
    def get(self, chat_id):

        chat_member = is_current_user_in_chat(chat_id)
        if not chat_member:
            raise Forbidden
        
        # there might be a better way of doing this
        chat = Chat.query.get(chat_id)
        return api_response(chat.get_all(chat_member.employee_id, True), "Got chat info")


class ChatGetMessageResource(Resource):
    @jwt_required()
    def get(self, message_id):
        message = Message.query.get(message_id)
        if not message:
            abort(404, "Message not found")
        chat_member = is_current_user_in_chat(chat_id=message.chat_id)
        if not chat_member:
            raise Forbidden
        return api_response(message.get_all(chat_member.employee_id), "Got message info")


class ChatSendMessageResource(Resource):
    @jwt_required()
    def post(self):
        try:
            data = request.get_json()
            message_id = data.get("message_id")

            if message_id:
                # for old message, i.e reply
                message = Message.query.get(message_id)
                if not message:
                    return api_abort(404, "No such message exist")
                chat_id = message.chat_id
                return_msg = "Reply message sent"
            else:
                # for new message
                chat_id = data.get("chat_id")
                if not chat_id:
                    return api_abort(400, "Must Provide a chat id to send message")
                return_msg = "Message sent"



            chat_member = is_current_user_in_chat(chat_id=chat_id)
            if not chat_member:
                raise Forbidden

            employee_id = chat_member.employee_id
            text = data.get("text")
            files = data.get("files")

            new_msg = Message.send_message(
                chat_id=chat_id,
                text=text,
                sender_id=employee_id,
                reply_to=message_id,
                files=files,
            )
            if not new_msg:
                abort(400)

            return api_response(new_msg.get_all(employee_id=employee_id), return_msg)

        except Exception as e:
            print(e)
            return api_abort(400, "Invalid Request")


class ChatListResource(Resource):
    @jwt_required()
    def get(self, company_id):
        company_employee = is_current_user_company_employee(company_id)
        if not company_employee:
            raise Forbidden

        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 10))
        query = request.args.get("query")
        chats = Chat.get_chats(
            company_id, company_employee.id, page=page, per_page=per_page, query=query
        )

        return api_response(chats, "Got list of chats")


class ChatMessageResource(Resource):
    @jwt_required()
    def get(self, chat_id):
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 10))
        query = request.args.get("query")

        chat_member = is_current_user_in_chat(chat_id) 
        if not chat_member:
            raise Forbidden

        messages = Message.get_messages(
            chat_id=chat_id, employee_id=chat_member.employee_id, per_page=per_page, page=page, query=query
        )
        # print(messages)
        return api_response(messages, "Got messages")


class ChatReadMessageResource(Resource):
    @jwt_required()
    def patch(self, message_id):
        try:
            message = Message.query.get(message_id)

            if message is None:
                return api_abort(404, f"No message with {message_id} is present")
            
            chat_member = is_current_user_in_chat(chat_id=message.chat_id)
            if not chat_member:
                raise Forbidden

            # data = request.get_json()

            # # this will be list of message ids?
            # message_id = data.get("message_id")


            employee_id = chat_member.employee_id
            message_status = MessageStatus.query.filter_by(
                message_id=message_id, employee_id=employee_id
            ).first()
            # if there's a message it has a status associated with it
            # so we don't need to check it
            # if not message_status:
            #     return api_abort(400, "Status wasn't created for the message")

            message_status.is_read = True
            message_status.update()
            # return api_response(message.get_all(employee_id=employee_id, short=True), "Message Read")
            return api_response(message.get_all(employee_id=employee_id), "Message Read")
        except Exception as e:
            return api_abort(500, str(e))


class ChatDeleteMessageResource(Resource):
    @jwt_required()
    def delete(self, message_id):
        try:
            # this needs more work
            message = Message.query.get(message_id)

            if not message:
                return api_abort(404, "No such Message exist")

            chat = Chat.query.get(message.chat_id)
            company_id = chat.company_id
            employee = is_current_user_company_employee(company_id)
            if not employee:
                raise Forbidden

            if message.sender_id == employee.id:
                data = request.get_json()
                delete_for_me = data.get("delete_for_me")
                if delete_for_me is None:
                    return api_abort(400, "Specify the type of delete to perform")
                if not delete_for_me:
                    message.delete()
                    return api_response([], "Message Deleted")

            status = MessageStatus.query.filter_by(
                message_id=message_id, employee_id=employee.id
            ).first()
            status.is_deleted = True
            status.update()

            return api_response("Message Hidden")
        except Exception as e:
            return abort(500, str(e))


class ChatEditMessageResource(Resource):
    @jwt_required()
    def put(self, message_id):
        try:
            data = request.get_json()
            text = data.get("text")
            files = data.get("files")

            message = Message.query.get(message_id)
            if message is None:
                abort(400, f"No message with {message_id} is present")
            
            chat_id = message.chat_id
            sender_id = message.sender_id
            chat_member = is_current_user_in_chat(chat_id)
            if not chat_member or (sender_id != chat_member.employee_id):
                raise Forbidden

            message.text = text
            message.is_edited = True
            message.update()

            if files:
                if files.get("removed"):
                    Message.remove_files(
                        message_id=message_id, file_ids=files["removed"]
                    )
                if files.get("added"):
                    Message.add_files(message_id=message_id, files=files["added"])

            return api_response(message.get_all(employee_id=chat_member.employee_id), "Message edited")

        except Exception as e:
            print(e)
            abort(400, str(e))


class PinMessageResource(Resource):
    @jwt_required()
    def post(self, message_id):

        message = Message.query.get(message_id)
        if not message:
            return api_abort(404, "No such message exist")

        chat_id = message.chat_id


        chat_member = is_current_user_in_chat(chat_id=chat_id)
        if not chat_member:
            raise Forbidden

        # if there's a message there's a chat
        chat = Chat.query.get(chat_id)

        # check if there's alrady a pin there
        pin_msg = PinnedMessages.query.filter_by(chat_id=chat.id, message_id=message.id).first()
        if pin_msg:
            return api_abort(400, "Message already pinned")

        # Pin the message
        pin_result = chat.pin(message)
        if pin_result:
            return api_response(chat.get_all(employee_id=chat_member.employee_id), "Message pinned successfully")
        else:
            abort(400, pin_result)


class ForwardMessageResource(Resource):
    @jwt_required()
    def post(self, message_id):
        data = request.get_json()

        # message_id = data.get("message_id")
        recipient_chat_ids = data.get("recipient_chat_ids")

        # Find the message to forward
        message = Message.query.get(message_id)
        if not message:
            return api_abort(404, "Message not found")
        
        # get the user from chat
        chat_id = message.chat_id
        chat_member = is_current_user_in_chat(chat_id=chat_id)
        if not chat_member:
            raise Forbidden
        sender_id = chat_member.employee_id
        
        if not (recipient_chat_ids and isinstance(recipient_chat_ids, list)):
            return api_abort(400, "Invalid request, need `recipient_chat_ids`")
        
        forwarded_messages = []
        for r_chat_id in recipient_chat_ids:
            # Get the recipient's chat
            recipient_chat = Chat.query.get(r_chat_id)

            # check if chat exist
            if not recipient_chat:
                continue

            # check if sender has access to that chat
            sender_in_chat = is_current_user_in_chat(r_chat_id)
            if not sender_in_chat:
                continue

            # for someone who is forwarding already forwarded message
            if message.forwarded:
                new_message = Message.send_message(
                    chat_id=r_chat_id,
                    sender_id=sender_in_chat.employee_id,
                    text=None,
                    files=None,
                    reply_to=None,
                    forwarded=message.forwarded
                )
            else:
                new_message = Message.send_message(
                    chat_id=r_chat_id,
                    sender_id=sender_in_chat.employee_id,
                    text=None,
                    files=None,
                    reply_to=None,
                    forwarded=message.id
                )
            forwarded_messages.append(new_message.get_all(sender_in_chat.employee_id))
            
        return api_response(result=forwarded_messages, description="Message Forwarded"
        )


class ChatStatusResource(Resource):
    # Update user typing status
    @jwt_required()
    def put(self, chat_id):
        # Get Chat
        chat = Chat.query.get(chat_id)
        if not chat:
            return api_abort(404, f"Chat does not exist")

        # Get Company
        company = Company.query.filter_by(id=chat.company_id).first()
        if not company:
            abort(404, f"No such company exist")

        # Check if user is company employee
        employee = Employee.query.filter_by(user_id=current_user.id, company_id=chat.company_id).first()
        if not employee:
            return api_abort(404, f"Employee does not exist")

        # Check if the user is in chat members
        chat_member = ChatMember.query.filter_by(chat_id=chat_id, employee_id=employee.id).first()
        if not chat_member:
            raise Forbidden

        # Update user typing status in the chat
        chat_member.last_typing_date = datetime.utcnow()

        # Update user in table
        chat_member.update()

        # Return response
        return api_response(description="User Typing Status updated", result={"status": "Ok"})

    # Check if the user is online and typing in the chat
    @jwt_required()
    def get(self, chat_id):
        # Get Chat
        chat = Chat.query.get(chat_id)
        if not chat:
            return api_abort(404, f"Chat does not exist")
        
        # Check if user is company employee
        employee = Employee.query.filter_by(user_id=current_user.id, company_id=chat.company_id).first()
        if not employee:
            raise Forbidden
        
        # Check if the user is in chat members
        chat_member = ChatMember.query.filter_by(chat_id=chat_id, employee_id=employee.id).first()
        if not chat_member:
            raise Forbidden
        
        # Get all chat members except current user
        all_chat_members = ChatMember.query.filter_by(chat_id=chat_id).all()
        if not all_chat_members:
            return api_abort(404, f"This chat has no members")
        # # Remove current user from chat members
        all_chat_members.remove(chat_member)
        
        all_statuses = []
        # Check online and typing status for each chat member in the all_chat_members
        for member in all_chat_members:
            employee = Employee.query.get(member.employee_id)
            user = User.query.get(employee.user_id)
            
            # if user.last_online_date and member.last_typing_date is not None:
            online_time_difference = datetime.utcnow() - user.last_online_date
            typing_time_difference = datetime.utcnow() - member.last_typing_date
            user_online_status = None
            user_typing_status = None
            
            # If user was last online 5 seconds ago, user is offline
            if online_time_difference > timedelta(seconds=5):
                user_online_status = False
            # Else User is online
            else:
                user_online_status = True
            
            # If user was last typing 5 seconds ago, user is not typing anymore
            if typing_time_difference > timedelta(seconds=5):
                user_typing_status = False
            # Else User is typing
            else:
                user_typing_status = True
            
            # Append all statuses to a list
            all_statuses.append({
                "is_typing": user_typing_status,
                "is_online": user_online_status,
                "time_difference": str(online_time_difference),
                "employee_id": member.employee_id})
        
        # Return results
        return api_response(description="Got chat user statuses", result=all_statuses)
