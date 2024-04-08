from datetime import datetime, timezone, timedelta
from sqlalchemy import (
    Column,
    String,
    Integer,
    ForeignKey,
    DateTime,
    Boolean,
    Float,
    Text,
    Unicode,
    and_,
    func,
    or_, Enum,
)
from sqlalchemy.orm import relationship, subqueryload, backref
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, abort, g, request
import logging
from flask_migrate import init, stamp, migrate, upgrade
import os, uuid, requests
from werkzeug.security import generate_password_hash, check_password_hash
from server.tools.assists import getconfig
from threading import Timer
from werkzeug.local import LocalProxy
from config import ApplicationConfig
from flask_jwt_extended import current_user

db = SQLAlchemy()


def get_random_avatar_link():
    return requests.get("https://xsgames.co/randomusers/avatar.php?g=male").url


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


def setup_db(app, restart=False):
    with app.app_context():
        db.app = app
        db.init_app(app)
        if restart:
            db.drop_all()
        db.create_all()

        def deploy():
            try:
                init()
            except:
                pass

            try:
                stamp()
                migrate()
                upgrade()
            except:
                raise

        deploy()


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


class User(db.Model):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)

    email = Column(String(100), nullable=False, unique=True)
    _password = Column(String, nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100))
    phone_number = Column(String(100))

    avatar = Column(Text)

    registered_date: datetime = Column(DateTime, default=datetime.utcnow)
    is_online = Column(Boolean, nullable=False, default=False)

    confirmed_on = Column(DateTime)

    last_online_date = Column(DateTime, default=datetime.utcnow)

    companies = relationship("Company")

    @property
    def password(self):
        print("Password can not be read.")

    @password.setter
    def password(self, password):
        self._password = generate_password_hash(password, method="sha256")

    def verify_password(self, password):
        return check_password_hash(self._password, password)

    def set_online(self):
        self.is_online = True
        self.update()

        def make_user_offline():
            with db.app.app_context():
                dbuser = User.query.get(self.id)
                dbuser.is_online = False
                dbuser.update()

        t = Timer(
            ApplicationConfig.ENDPOINT_MAKE_USER_OFFLINE_AFTER_N_SECONDS,
            make_user_offline,
        )
        t.start()

    @property
    def name(self):
        if self.last_name:
            return f"{self.first_name} {self.last_name}"
        return  self.first_name

    def insert(self):
        self.email = self.email.lower()
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def get_all(self, short=False):
        companies = [
            Company.query.get(i).get_all()
            for i in [
                i.company_id for i in Employee.query.filter_by(user_id=self.id).all()
            ]
        ]

        if short:
            return {
                "user_id": self.id,
                "email": self.email,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "companies": companies,
                "avatar": self.avatar,
            }
        return {
            "user_id": self.id,
            # "external_id": self.external_id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "companies": companies,
            "phone_number": self.phone_number,
            # "role": self.role,
            # "is_admin": self.is_admin,
            "registered_date": self.registered_date.timestamp(),
            # "is_active": self.is_active,
            "is_online": self.is_online,
            "avatar": self.avatar,
            "confirmed_on": self.confirmed_on.timestamp(),
            "last_online_date": self.last_online_date.timestamp()
    
        }

    def __repr__(self):
        return "<User %r>" % self.id


class Navbar(db.Model):
    __tablename__ = "navbars"
    employee_id = Column(Integer, ForeignKey("employees.id"), primary_key=True)

    hierarchy = Column(Boolean, nullable=False, default=False)
    employees = Column(Boolean, nullable=False, default=False)
    search_workers = Column(Boolean, nullable=False, default=False)
    chats = Column(Boolean, nullable=False, default=False)

    # Projects Departmnet
    projects = Column(Boolean, nullable=False, default=False)
    pipelines = Column(Boolean, nullable=False, default=False)
    my_tasks = Column(Boolean, nullable=False, default=False)
    statistics = Column(Boolean, nullable=False, default=False)
    # project_stats = Column(Boolean, nullable=False, default=False)

    # Purchase Department
    purchases = Column(Boolean, nullable=False, default=False)
    providers = Column(Boolean, nullable=False, default=False)
    customers = Column(Boolean, nullable=False, default=False)
    products = Column(Boolean, nullable=False, default=False)
    orders = Column(Boolean, nullable=False, default=False)

    # Sales Department
    sales = Column(Boolean, nullable=False, default=False)
    forecasts = Column(Boolean, nullable=False, default=False)
    # sales_stats = Column(Boolean, nullable=False, default=False)

    # Finance Department
    finance = Column(Boolean, nullable=False, default=False)
    accounts = Column(Boolean, nullable=False, default=False)
    flow_and_funds = Column(Boolean, nullable=False, default=False)
    mutual_settlements = Column(Boolean, nullable=False, default=False)
    # finance_stats = Column(Boolean, nullable=False, default=False)

    # Warehouse Department
    warehouses = Column(Boolean, nullable=False, default=False)
    stock_lists = Column(Boolean, nullable=False, default=False)
    planned_shipments = Column(Boolean, nullable=False, default=False)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Tag(db.Model):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    color = Column(String)
    text = Column(String, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def get_all(self, short=False):
        if short:
            return {
                "color": self.color,
                "text": self.text,
                "date": self.date.timestamp(),
            }
        return {
            "id": self.id,
            "company_id": self.company_id,
            "color": self.color,
            "text": self.text,
            "date": self.date.timestamp(),
        }


class Notification(db.Model):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    # type: 'system', 'message', ...
    type = Column(String)

    # type = system
    title = Column(String)
    description = Column(String)

    is_read = Column(Boolean, nullable=False, default=False)

    date = Column(DateTime, default=datetime.utcnow)
    
    avatar = Column(Text)

    def get_all_unread_msgs(employee_id):
        messages = (
            Message.query.join(Chat, Message.chat_id == Chat.id)
            .join(ChatMember, Chat.id == ChatMember.chat_id)
            .join(MessageStatus, MessageStatus.message_id == Message.id)
            .filter(
                and_(ChatMember.employee_id == employee_id, MessageStatus.is_read == False)
            )
        )
        return [
            {
                "chat_id": message.chat_id,
                "message_id": message.id,
                "type": "new_message",
            }
            for message in messages
        ]
    
    def get_all(self, short=False):
        if short:
            return {
                "user_id": self.user_id,
                "type": self.type,
                "description": self.description,
                "title": self.title 
            # "date": self.date
            }        
        return {
            "id": self.id,
            "user_id": self.user_id,
            "type": self.type,
            "title": self.type,
            "description": self.description,
            "date": self.date.timestamp(),
            "is_read": self.is_read,
        }
    
    @classmethod
    def get_unread_nots(cls, user_id):
        unread_nots: list[Notification] = Notification.query.filter_by(user_id=user_id, is_read=False).order_by(Notification.date.desc()).all()
        for nots in unread_nots:
            # once we get the nots now they are read
            nots.is_read = True
            nots.update()
        return [notification.get_all(True)
                for notification in unread_nots
            ]

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class PhoneNumber(db.Model):
    __tablename__ = "phone_numbers"
    id = Column(Integer, primary_key=True)
    phone_number = Column(String(16))
    company_id = Column(Integer, ForeignKey("companies.id"))


class Email(db.Model):
    __tablename__ = "emails"
    id = Column(Integer, primary_key=True)
    email = Column(String(100))
    company_id = Column(Integer, ForeignKey("companies.id"))


class Company(db.Model):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True)

    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    name = Column(String(100), nullable=False)
    name_in_law = Column(String(512), nullable=False)
    # login = Column(String(100), unique=True, nullable=False)
    # backref to be able to get the company from the PhoneNumber model
    phone_numbers = relationship("PhoneNumber", backref="company")
    # phone_number = Column(String(16), unique=True, nullable=False)
    emails = relationship("Email", backref="company")
    # email = Column(String(100), unique=True, nullable=False)
    avatar = Column(Text)

    created_date = Column(DateTime, default=datetime.utcnow)

    # TODO:why not create a backref here, we can access the company from the Employee table and we won't waste
    # a query operation
    employees = relationship("Employee")

    def insert(self):
        db.session.add(self)
        db.session.commit()
        new_Employee = Employee(
            user_id=self.owner_id, company_id=self.id, position="CEO"
        )
        new_Employee.insert()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def get_all(self, short=False):
        if short:
            return {
                "company_id": self.id,
                "name": self.name,
                "owner_id": self.owner_id,
                "avatar": self.avatar,
            }
        return {
            "company_id": self.id,
            "name": self.name,
            "name_in_law": self.name_in_law,
            "owner_id": self.owner_id,
            "avatar": self.avatar,
        }

    def __repr__(self):
        return "<Company %r>" % self.id


class Employee(db.Model):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    # position: worker, assistant, manager ...
    position = Column(String(64), default="worker", nullable=False)
    wage = Column(Float)
    work_hour = Column(Float)
    date = Column(DateTime, default=datetime.utcnow)

    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    leader_id = Column(Integer)

    user = relationship("User")

    def insert(self):
        db.session.add(self)
        db.session.commit()
        if self.leader_id:
            next_leader_id = self.leader_id
            loops = 0
            while next_leader_id:
                loops += 1
                if loops > 10**5:
                    break
                empl_lead = EmployeeLeader(
                    employee_id=self.id, leader_id=next_leader_id
                )
                empl_lead.insert()
                next_leader_id = Employee.query.get(next_leader_id).leader_id

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def get_all(self, short=False):
        if not self.user_id:
            tail = {"name": None, "avatar": None}
        else:
            user: User = User.query.get(self.user_id)
            if not user:
                tail = {"name": None, "avatar": None}
            # tail = {"name": f"{user.first_name} {user.last_name}" if user.last_name else user.first_name, "avatar": user.avatar}
            tail = {"name": user.name, "avatar": user.avatar}

        team = False
        if EmployeeLeader.query.filter_by(leader_id=self.id).all() != []:
            team = True

        if short:
            return {
                "employee_id": self.id,
                "user_id": self.user_id,
                "position": self.position,
                "team": team,
            } | tail

        return {
            "employee_id": self.id,
            "user_id": self.user_id,
            "position": self.position,
            "company_id": self.company_id,
            "leader_id": self.leader_id,
            "team": team,
        } | tail

    def __repr__(self):
        return "<Employee %r>" % self.id


class EmployeeLeader(db.Model):
    __tablename__ = "employee_leader"
    id = Column(Integer, primary_key=True)
    leader_id = Column(Integer, ForeignKey("employees.id"), nullable=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=True)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def get_all(self, short=False):
        if short:
            return {
                "id": self.id,
                "employee_id": self.employee_id,
                "leader_id": self.leader_id,
            }

        return {
            "id": self.id,
            "employee_id": self.employee_id,
            "leader_id": self.leader_id,
        }

    def __repr__(self):
        return "<EmployeeLeader %r>" % self.id


class CompanyInvitation(db.Model):
    __tablename__ = "companies_invitations"
    id = Column(Integer, primary_key=True)
    token = Column(String, nullable=False)
    email = Column(String, nullable=False)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    date = Column(DateTime, default=datetime.utcnow)

    def is_valid(self):
        return (
            datetime.utcnow()
            < self.date + ApplicationConfig.EXP_TIME_INVITATION_LINK_OF_COMPANY
        )

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<CompanyInvitation %r>" % self.id


class PinnedMessages(db.Model):
    __tablename__ = "pinned_messages"
    chat_id = Column(Integer, ForeignKey("chats.id"), primary_key=True)
    message_id = Column(Integer, ForeignKey("messages.id"), primary_key=True)

    # only use I could find here
    pinned_date = Column(DateTime, default=datetime.now())

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Chat(db.Model):
    __tablename__ = "chats"
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)

    # for groups only
    name = Column(String)
    owner_id = Column(Integer, ForeignKey("employees.id"))

    members: list = relationship("ChatMember")

    # lazy=dynamic to return the query instead of the whole date here
    messages = relationship("Message", lazy="dynamic")
    date: datetime = Column(DateTime, default=datetime.utcnow)
    
    last_update_at = Column(DateTime, default=datetime.utcnow)

    # why create a association table here?
    pinned_messages = relationship(
        "Message", secondary="pinned_messages", lazy="dynamic"
    )

    is_group = Column(Boolean, default=False)

    avatar = Column(Text)


    @classmethod
    def get_chats(cls, company_id, employee_id, page=1, per_page=10, query=None):
        # db.session.query(Chat, func.count(Message.id).label("unread_count")
        #                  .join(ChatMember, Chat.id == ChatMember.chat_id).
        #                  .join(Company, )
        #                  )
        
        if query:
            unread_messages = (
                # perhaps add a order_by here to order chats
                db.session.query(Chat, func.count(Message.id).label("unread_count"))
                .outerjoin(ChatMember, and_(Chat.id == ChatMember.chat_id, ChatMember.employee_id == employee_id))
                .outerjoin(Message, Chat.id == Message.chat_id)
                .outerjoin(
                    MessageStatus,
                    and_(
                        Message.id == MessageStatus.message_id,
                        MessageStatus.is_read == False,
                    ),
                ).filter(
                    Chat.name.ilike(f"%{query}%")
                )
                .group_by(Chat)
                # .order_by(Chat.last_update_at.desc())
                .paginate(per_page=per_page, page=page, error_out=False)
                .items
            )
        else:
            unread_messages = (
                # perhaps add a order_by here to order chats
                db.session.query(Chat, func.count(Message.id).label("unread_count"))
                .outerjoin(ChatMember, and_(Chat.id == ChatMember.chat_id, ChatMember.employee_id == employee_id))
                .outerjoin(Message, Chat.id == Message.chat_id)
                .outerjoin(
                    MessageStatus,
                    and_(
                        Message.id == MessageStatus.message_id,
                        MessageStatus.is_read == False,
                    ),
                )
                .group_by(Chat)
                # .order_by(Chat.last_update_at.desc())
                .paginate(per_page=per_page, page=page, error_out=False)
                .items
            )

        chats = [
            chat.get_all(employee_id, True) | {"unread_count": unread_count}
            for chat, unread_count in unread_messages
        ]

        return chats

    @classmethod
    def get_all_chats(cls, company_id, employee_id):
        from sqlalchemy import case

        chats = (
            db.session.query(
                Chat.id,
                Chat.name,
                func.concat(User.first_name, " ", User.last_name).label("user_name"),
                Message.text,
                MessageStatus.date,
                MessageStatus.is_read,
                func.count(
                    case(
                        [
                            (
                                (MessageStatus.is_read == False)
                                & (Message.sender_id != employee_id),
                                1,
                            )
                        ]
                    )
                ).label("unread_messages_count"),
            )
            .join(ChatMember, ChatMember.chat_id == Chat.id)
            .join(Employee, ChatMember.employee_id == Employee.id)
            .outerjoin(User, Chat.owner_id == User.id)
            .outerjoin(Message, Chat.id == Message.chat_id)
            .outerjoin(
                MessageStatus,
                (Message.id == MessageStatus.message_id)
                & (MessageStatus.employee_id == employee_id),
            )
            .group_by(
                Chat.id,
                Chat.name,
                User.first_name,
                User.last_name,
                Message.text,
                MessageStatus.date,
                MessageStatus.is_read,
            )
            .filter(Employee.id == employee_id)
            .all()
        )

        return [
            {
                "chat_id": i[0],
                "name": i[1],
                "user_name": i[2],
                "last_message": i[3],
                "is_read": i[4],
                "unread_count": i[5],
            }
            for i in chats
        ]

    def relates(self, user_id) -> bool:
        return user_id in [
            Employee.query.get(i.employee_id).user_id for i in self.members
        ]

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


    def get_all(self, employee_id, short=False):
        tail = {
            "chat_id": self.id,
            "name": self.name,
            "date": self.date.timestamp(),
            "avatar": self.avatar,
            "is_group": self.is_group,
            "participants": [mem.get_all(short=True) for mem in self.members]
        }
        if not self.is_group:
            member = [member for member in self.members if member.employee.id != employee_id][0]
            # name = member.employee.user.first_name
            tail.update({"name": member.employee.user.name, "avatar": member.employee.user.avatar})

        if not short:
            tail.update(
                    {"company_id": self.company_id,
                     "last_message": self.messages.order_by(Message.date.desc()).first()}
                )
            if lm := tail["last_message"]:
                msg_status = MessageStatus.query.filter_by(
                    message_id=lm.id
                ).first()
                #
                tail["last_message"] = tail["last_message"].get_all(employee_id)
                # tail["last_message"].update({"is_read": msg_status.is_read})
        return tail

    def pin(self, message):
        pin_msg = PinnedMessages(chat_id=self.id, message_id=message.id)
        pin_msg.insert()
        return pin_msg

    def __repr__(self):
        return "<Chat %r>" % self.id


class ChatMember(db.Model):
    __tablename__ = "chat_members"
    id = Column(Integer, primary_key=True)
    # chat_id is for both private chats and group chats
    chat_id = Column(Integer, ForeignKey("chats.id"), nullable=False)

    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)

    last_typing_date = Column(DateTime, default=datetime.utcnow)
    notification = Column(Boolean, default=True)

    employee = relationship("Employee")

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def get_all(self, short=False):
        _user_id = Employee.query.get(self.employee_id).user_id
        user = User.query.get(_user_id)
        if short:
            return {
                "employee_id": self.id,
                "name": user.name,
                "avatar": user.avatar,
            }
        return {
            "employee_id": self.id,
            "name": user.name,
            "avatar": user.avatar,
            "last_typing_date": self.last_typing_date
        }

    def __repr__(self):
        return "<ChatMember %r>" % self.id


class Message(db.Model):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, ForeignKey("chats.id"), nullable=False)

    sender_id = Column(Integer, ForeignKey("employees.id"), nullable=False)

    # for text msg
    text = Column(Unicode)

    date: datetime = Column(DateTime, default=datetime.utcnow)
    reply_to = Column(Integer, ForeignKey("messages.id"), nullable=True)

    is_edited = Column(Boolean, nullable=False, default=False)

    readers = relationship("MessageStatus")
    sender = relationship("Employee")
    message_files = relationship(
        "MessageFile",
        backref=backref("message", uselist=False),
        cascade="all, delete-orphan",
    )
    forwarded = Column(Integer, ForeignKey("messages.id"), nullable=True)

    @classmethod
    def send_message(
        cls,
        chat_id,
        sender_id,
        text: str = None,
        files: str = None,
        reply_to=None,
        forwarded=None
    ):
        try:
            new_msg = cls(
                chat_id=chat_id, text=text, sender_id=sender_id, reply_to=reply_to, forwarded=forwarded
            )
            new_msg.insert()

            members = ChatMember.query.filter_by(chat_id=chat_id).all()

            # new_msg_statuses = [i.employee_id for i in members]
            # new_msg_statuses = [i for i in members]
            sender: User = Employee.query.get(sender_id).user
            for i in members:
                if sender_id == i.employee_id:
                    new_msg_status = MessageStatus(message_id=new_msg.id, employee_id=i.employee_id, is_read=True, is_delivered=True)
                else:
                    new_msg_status = MessageStatus(message_id=new_msg.id, employee_id=i.employee_id)
                    if i.notification:

                        new_notification = Notification(
                                user_id=i.id,
                                type='message',
                                title=f'New Message from {sender.name}', 
                                description=text, 
                                is_read=False, 
                                avatar=sender.avatar
                                )
                        new_notification.insert()
                new_msg_status.insert()

            Message.add_files(new_msg.id, files)

            # update the chat object
            current_chat = Chat.query.get(chat_id)
            current_chat.last_update_at = datetime.now(timezone.utc)
            current_chat.update()

            return new_msg
        except:
            raise

    @classmethod
    def add_files(cls, message_id, files):
        if files and isinstance(files, list):
            for file in files:
                new_msg_file = MessageFile(
                    message_id=message_id,
                    file=file.get("file"),
                    name=file.get("fileName"),
                    _type=file.get("fileType"),
                )
                new_msg_file.insert()

    @classmethod
    def remove_files(cls, message_id, file_ids):
        if file_ids and isinstance(file_ids, list):
            for file_id in file_ids:
                target_file = MessageFile.query.filter_by(
                    message_id=message_id, id=file_id
                ).first()
                if target_file:
                    target_file.delete()
                else:
                    # in case such file doesn't even exist
                    continue

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def get_all(self, employee_id, short=False):
        forwarded = None
        if self.forwarded:
            forwarded = Message.query.get(self.forwarded).get_all(employee_id, True)
        
        if short:
            return {
                "message_id": self.id,
                "text": self.text,
                "sender_name": self.sender.get_all(True)["name"],
                "files": [
                    {**i.get_all(), "size": len(i.file)} for i in self.message_files
                ],
            }
        return {
            "message_id": self.id,
            "text": self.text,
            "readers": [i.get_all(True) for i in self.readers],
            "chat_id": self.chat_id,
            "sender_id": self.sender_id,
            "is_edited": self.is_edited,
            # we'll get is read from above
            # "is_read": MessageStatus.query.filter_by(message_id=self.id, employee_id=employee_id).first().is_read,
            "replied": self.reply_to,
            "date": self.date.timestamp(),
            "files": [{**i.get_all(), "size": len(i.file)} for i in self.message_files],
            "forwarded": forwarded
        }

    @classmethod
    def get_messages(cls, chat_id, employee_id, per_page=10, page=1, query=None):
        if not query:
            messages = (
                db.session.query(Message)
                .filter_by(chat_id=chat_id)
                .join(MessageStatus, Message.id == MessageStatus.id)
                .filter(MessageStatus.is_deleted == False)
                .order_by(Message.date.desc())
                .paginate(per_page=per_page, page=page, error_out=False)
                .items
            )
        else:
            messages = (
                db.session.query(Message)
                .filter_by(chat_id=chat_id)
                .join(MessageStatus, Message.id == MessageStatus.id)
                .filter(
                    and_(
                        MessageStatus.is_deleted == False,
                        Message.text.ilike(f"%{query}%"),
                    )
                )
                .order_by(Message.date.desc())
                .paginate(per_page=per_page, page=page, error_out=False)
                .items
            )

        return [msg.get_all(employee_id=employee_id, short=True) for msg in messages]

    def __repr__(self):
        return "<Message %r>" % self.id


class MessageStatus(db.Model):
    __tablename__ = "message_status"
    id = Column(Integer, primary_key=True)

    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=True)
    message_id = Column(Integer, ForeignKey("messages.id"), nullable=True)
    is_read = Column(Boolean, default=False)
    is_delivered = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)

    date: datetime = Column(DateTime, default=datetime.utcnow)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def get_all(self, short=False):
        if short:
            return {
                "employee_id": self.employee_id,
                "is_read": self.is_read,
                "is_delivered": self.is_delivered,
            }
        return {
            "id": self.id,
            "message_id": self.message_id,
            "employee_id": self.employee_id,
            "is_read": self.is_read,
            "is_delivered": self.is_delivered,
        }
    
    @classmethod
    def get_all_not_delivered_messages(self, employee_id):
        msgs = db.session.query(Message).join(Employee, Employee.id == employee_id).join(MessageStatus, and_(MessageStatus.message_id == Message.id, MessageStatus.is_delivered == False)).order_by(Message.date.desc()).all()
        return [msg.get_all(employee_id, True) for msg in msgs]

    def __repr__(self):
        return "<MessageStatus %r>" % self.id


class MessageFile(db.Model):
    __tablename__ = "messages_files"
    id = Column(Integer, primary_key=True)

    message_id = Column(Integer, ForeignKey("messages.id"), nullable=False)

    name = Column(String, nullable=False)

    # binaries : Text | LargeBinary
    file = Column(Text, nullable=False)

    _type = Column(String, nullable=False)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def get_all(self, short=False):
        if short:
            return {"file": self.file, "name": self.name, "type": self._type}
        return {
            "id": self.id,
            "message_id": self.message_id,
            "file": self.file,
            "type": self._type,
            "name": self.name,
        }

    def __repr__(self):
        return "<MessageFile %r>" % self.id


class Pipeline(db.Model):
    __tablename__ = 'pipelines'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    company = relationship('Company', cascade='all, delete', backref='pipelines', lazy=True)
    
    def insert(self):
        db.session.add(self)
        db.session.commit()


class PipelineStage(db.Model):
    __tablename__ = 'pipeline_stages'
    id = Column(Integer, primary_key=True)
    pipeline_id = Column(Integer, ForeignKey('pipelines.id'), nullable=False)
    order_number = Column(Integer, nullable=False)
    name = Column(String(100), nullable=False)
    
    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def __repr__(self):
        return f"<Stage {self.id}>"


class Project(db.Model):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True)
    stage_id = Column(Integer, ForeignKey("pipeline_stages.id"))
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    counter_party = Column(String(100), nullable=False)
    budget = Column(Float, nullable=False)
    currency = Column(String(20), nullable=False)
    status = Column(Enum(
        "assigned", "active", "succeeded", "failed",
        name="ProjectStatus"),
        nullable=False, default="assigned")
    
    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    def get_all(self, short=False):
        if short:
            return {
                "stage_id": self.stage_id,
                "counter_party": self.counter_party,
                "name": self.name,
                "description": self.description,
                "budget": self.budget,
                "currency": self.currency,
                "status": self.status,
            }
        return {
            "stage_id": self.stage_id,
            "counter_party": self.counter_party,
            "name": self.name,
            "description": self.description,
            "budget": self.budget,
            "currency": self.currency,
            "status": self.status,
        }


class ProjectTask(db.Model):
    __tablename__ = "project_tasks"
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)

    title = Column(String, nullable=False)
    description = Column(String)
    
    status = Column(Enum(
        "assigned", "active", "succeeded", "failed",
        name="TaskStatus"),
        nullable=False, default="assigned")

    date = Column(DateTime, default=datetime.utcnow)
    due_date = Column(DateTime)

    task_tags = relationship("ProjectTaskTag")
    task_members = relationship("ProjectTaskMember")

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def get_all(self, short=False):
        if short:
            return {
                "project_id": self.project_id,
                "title": self.title,
                "description": self.description,
                "status": self.status,
                "date": self.date.timestamp(),
                "due_date": self.due_date.timestamp(),
                "task_tags": [i.get_all(True) for i in self.task_tags],
                "task_members": [i.get_all(True) for i in self.task_members]
            }
        return {
            "id": self.id,
            "project_id": self.project_id,
            "title": self.title,
            "description": self.description,
			"status": self.status,
            "date": self.date.timestamp(),
            "due_date": self.due_date.timestamp(),
            "task_tags": [i.get_all(True) for i in self.task_tags],
            "task_members": [i.get_all(True) for i in self.task_members]
        }

    # Get the tasks along with its tags and task members, ordered, paginated and categorized by their statuses
    @classmethod
    def get_tasks(cls, employee_id=None, project_id=None, page=1, per_page=10):
        # Task statuses
        statuses = ["assigned", "active", "succeeded", "failed"]
        
        # Dict to store all tasks data
        tasks_data = {}

        # If getting tasks of a project
        if project_id:
            # Get all tasks of the project categorized, ordered and paginated.
            for status in statuses:
                tasks = (
                    db.session.query(ProjectTask).filter(
                        ProjectTask.project_id == project_id, ProjectTask.status == status).order_by(
                        ProjectTask.date.desc()))
                
                # Add tasks to the dictionary
                tasks_data[status] = [task.get_all() for task in tasks]
        
        # If getting tasks of an employee
        elif employee_id:
            for status in statuses:
                # Get all tasks of the employee categorized, ordered and paginated.
                tasks = (
                    db.session.query(ProjectTask).join(
                        ProjectTaskMember,
                        ProjectTaskMember.employee_id == employee_id).filter(
                        ProjectTask.status == status).order_by(
                        ProjectTask.date.desc()).paginate(
                        per_page=per_page, page=page, error_out=False).items)
                
                # Add tasks to the dictionary
                tasks_data[status] = [task.get_all() for task in tasks]
            
        # Return the tasks data
        return tasks_data

    def __repr__(self):
        return "<ProjectTask %r>" % self.id


class ProjectTaskTag(db.Model):
    __tablename__ = "project_task_tags"
    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey("project_tasks.id", ondelete="CASCADE"), nullable=False)
    tag_id = Column(Integer, ForeignKey("tags.id"), nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    tag = relationship("Tag")
    

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def get_all(self, short=False):
        if short:
            return {
                "tag_color": self.tag.color,
                "tag_text": self.tag.text,
                "date": self.date.timestamp(),
            }
        return {
            "id": self.id,
            "tag_id": self.tag_id,
            "tag_color": self.tag.color,
            "tag_text": self.tag.text,
            "date": self.date.timestamp(),
        }

    def __repr__(self):
        return "<ProjectTaskTag %r>" % self.id


class ProjectTaskMember(db.Model):
    __tablename__ = "project_task_members"
    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey("project_tasks.id", ondelete="CASCADE"), nullable=False)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    date = Column(DateTime, default=datetime.utcnow)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def get_member(self):
        return {
            "employee_id": self.employee_id,
            "name": User.query.get(Employee.query.get(self.employee_id).user_id).first_name,
            "avatar": User.query.get(Employee.query.get(self.employee_id).user_id).avatar,
        }

    def get_all(self, short=False):
        if short:
            return {
                "id": self.id,
                "task_id": self.task_id,
                "employee_id": self.employee_id,
            }
        return {
            "id": self.id,
            "task_id": self.task_id,
            "employee_id": self.employee_id,
            "date": self.date.timestamp(),
        }

    def __repr__(self):
        return "<ProjectTaskMember %r>" % self.id


class ProjectTaskComment(db.Model):
    __tablename__ = "project_task_comments"
    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey("project_tasks.id", ondelete="CASCADE"), nullable=False)

    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    text = Column(String, nullable=False)

    date = Column(DateTime, default=datetime.utcnow)

    employee = relationship("Employee")

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_comments(cls, task_id, employee_id, per_page=10, page=1):
        # Get the task comments based on task_id in paginated order
        task_comments = ProjectTaskComment.query.filter_by(
            employee_id=employee_id,
            task_id=task_id).order_by(
            ProjectTaskComment.date.desc()).paginate(
            per_page=per_page, page=page, error_out=False).items
    
        # Put the comments in a list
        comments = [attachment.get_all(True) for attachment in task_comments]
    
        # Return the comments
        return comments

    def get_all(self, short=False):
        if short:
            return {
                "task_id": self.task_id,
                "employee_id": self.employee_id,
                "text": self.text,
                "date": self.date.timestamp(),
            }
        return {
            "id": self.id,
            "task_id": self.task_id,
            "employee_id": self.employee_id,
            "text": self.text,
            "date": self.date.timestamp(),
            "employee": self.employee.get_all(True),
        }

    def __repr__(self):
        return "<ProjectTaskComment %r>" % self.id


class ProjectTaskAttachment(db.Model):
    __tablename__ = "project_task_attachments"
    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey("project_tasks.id", ondelete="CASCADE"), nullable=False)

    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)

    # binaries: Text | LargeBinary
    file = Column(Text, nullable=False)
    text = Column(String, nullable=False)

    date = Column(DateTime, default=datetime.utcnow)

    employee = relationship("Employee")

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_attachments(cls, task_id, employee_id, per_page=10, page=1):
        # Get the task attachments based on task_id in paginated order
        task_attachments = ProjectTaskAttachment.query.filter_by(
            employee_id=employee_id,
            task_id=task_id).order_by(
            ProjectTaskAttachment.date.desc()).paginate(
            per_page=per_page, page=page, error_out=False).items
    
        # Put the attachments in a list
        attachments = [attachment.get_all(True) for attachment in task_attachments]
        
        # Return the attachments
        return attachments
    
    def get_all(self, short=False):
        if short:
            return {
                "task_id": self.task_id,
                "employee_id": self.employee_id,
                "text": self.text,
                "file": self.file,
            }
        return {
            "id": self.id,
            "task_id": self.task_id,
            "employee_id": self.employee_id,
            "text": self.text,
            "file": self.file,
            "date": self.date.timestamp(),
            "employee": self.employee.get_all(True),
        }

    def __repr__(self):
        return "<ProjectTaskAttachment %r>" % self.id


class Provider(db.Model):
    __tablename__ = "providers"
    id = Column(Integer, primary_key=True)
    
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=True)
    counter_party = Column(Integer, ForeignKey("companies.id"), nullable=False)
    created = Column(DateTime, default=datetime.utcnow)
    last_deal_with = Column(DateTime, default=datetime.utcnow)
    description = Column(Text, nullable=False)
    name = Column(Text, nullable=False)
    avatar = Column(Text, nullable=False)
    
    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def get_all(self, short=False):
        if short:
            return {
                "name": self.name,
                "avatar": self.avatar,
                "description": self.description,
                "company_id": self.company_id,
                "counter_party": self.counter_party,
                "created": self.created.timestamp(),
                "last_deal_with": self.last_deal_with.timestamp(),
            }
        return {
            "id": self.id,
            "name": self.name,
            "avatar": self.avatar,
            "description": self.description,
            "company_id": self.company_id,
            "counter_party": self.counter_party,
            "created": self.created.timestamp(),
            "last_deal_with": self.last_deal_with.timestamp(),
        }

    @classmethod
    def get_providers(cls, types, name, company_id, per_page=10, page=1):
        # Get provider data and send it in paginated order
        providers_data = []
        
        # If filter types are not selected
        if not types:
            # And if name is not searched
            if not name:
                # Get all providers of the company
                providers = (
                    db.session.query(Provider).filter_by(
                        counter_party=company_id).order_by(
                        Provider.last_deal_with.desc()).paginate(
                        per_page=per_page, page=page, error_out=False).items)
            # And if name is searched
            else:
                # Search the providers by name
                providers = (
                    db.session.query(Provider).filter(
                        Provider.name.ilike(f"%{name}%"),
                        Provider.counter_party == company_id).order_by(
                        Provider.last_deal_with.desc()).paginate(
                        per_page=per_page, page=page, error_out=False).items)
    
            # Return the providers in a list
            return [provider.get_all(True) for provider in providers]
        # Else, if filter types are selected
        else:
            # And If name is not searched
            if not name:
                # for each provider type get all the providers with the same company of the user
                for provider_type in types:
                    providers = db.session.query(Provider).join(
                        ProviderType, ProviderType.type == provider_type).filter(
                        Provider.id == ProviderType.provider_id,
                        Provider.counter_party == company_id).order_by(
                        Provider.created.desc()).paginate(
                        per_page=per_page, page=page, error_out=False).items
                    # If providers exist
                    if providers:
                        # append the providers to the list
                        providers_data.append([provider.get_all(True) for provider in providers])
                # Return the providers
                return providers_data
            # Else, If filter types are selected and name is also searched
            else:
                # for each provider types, then get search those providers by name and return the results
                for provider_type in types:
                    providers = db.session.query(Provider).join(
                        ProviderType, ProviderType.type == provider_type).filter(
                        Provider.id == ProviderType.provider_id,
                        Provider.counter_party == company_id,
                        Provider.name.ilike(f"%{name}%")).order_by(
                        Provider.created.desc()).paginate(
                        per_page=per_page, page=page, error_out=False).items
                    # If providers exist
                    if providers:
                        # append the providers to the list
                        providers_data.append([provider.get_all(True) for provider in providers])
                # Return the providers
                return providers_data
            

class ProviderType(db.Model):
    __tablename__ = "provider_types"
    id = Column(Integer, primary_key=True)
    
    provider_id = Column(Integer, ForeignKey("providers.id"), nullable=False)
    type = Column(Text, nullable=False)
    
    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def get_all(self, short=False):
        if short:
            return {
                "provider_id": self.provider_id,
                "type": self.type
            }
        return {
            "id": self.id,
            "provider_id": self.provider_id,
            "type": self.type
        }


class Warehouse(db.Model):
    __tablename__ = "warehouses"
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    coordinates = Column(Text)
    
    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()
    
    def get_all(self, short=False):
        if short:
            return {
                "company_id": self.company_id,
                "coordinates": self.coordinates}
        return {
            "id": self.id,
            "company_id": self.company_id,
            "coordinates": self.coordinates}


class Product(db.Model):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    provider_id = Column(Integer, ForeignKey("providers.id"))
    company_id = Column(Integer, ForeignKey("companies.id"))
    avatar = Column(Text)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    currency = Column(String(20), nullable=False)
    description = Column(Text)
    images = relationship("ProductImage", backref="products")
    
    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def get_all(self, short=False):
        if short:
            return {
                "avatar": self.avatar,
                "name": self.name,
                "price": self.price,
                "currency": self.currency,
                "description": self.description,
                "images": [i.get_all(True) for i in self.images],
                
            }
        return {
            "id": self.id,
            "avatar": self.avatar,
            "name": self.name,
            "price": self.price,
            "currency": self.currency,
            "description": self.description,
            "images": [i.get_all(True) for i in self.images],
        }


class ProductImage(db.Model):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True)
    image = Column(Text, nullable=False)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    
    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()
    
    def get_all(self, short=False):
        if short:
            return {
                "image": self.image,
            }
        return {
            "id": self.id,
            "image": self.image,
            "product_id": self.product_id,
        }


class WarehouseProduct(db.Model):
    __tablename__ = "warehouse_products"
    id = Column(Integer, primary_key=True)
    warehouse_id = Column(Integer, ForeignKey("warehouses.id", ondelete="CASCADE"))
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))
    product_quantity = Column(Integer, nullable=False, default=0)
    
    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()
    
    def get_all(self, short=False):
        if short:
            return {
                "warehouse_id": self.warehouse_id,
                "product_id": self.product_id,
                "product_quantity": self.product_quantity}
        return {
            "id": self.id,
            "warehouse_id": self.warehouse_id,
            "product_id": self.product_id,
            "product_quantity": self.product_quantity}


class Order(db.Model):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    provider_id = Column(Integer, ForeignKey("providers.id"))
    company_id = Column(Integer, ForeignKey("companies.id"))
    ordered_date = Column(DateTime, default=datetime.utcnow)
    status = Column(Enum(
        "paid", "cancelled", "refunded", "pending", "accepted",
        name="OrderStatus"), nullable=False,
        default="pending")
    # This will be set when order is paid
    tracking_status = Column(Enum(
        "ordered", "in_transit", "out_for_delivery", "delivered",
        name="Tracking"),
        nullable=True)
    items = relationship("OrderItem")

    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()
    
    def get_all(self, short=False):
        if short:
            return {
                "provider_id": self.provider_id,
                "status": self.status,
                "tracking_status": self.tracking_status,
                "ordered_date": self.ordered_date.timestamp(),
                "order_items": [i.get_all(True) for i in self.items],
    
            }
        return {
            "id": self.id,
            "provider_id": self.provider_id,
            "status": self.status,
            "tracking_status": self.tracking_status,
            "ordered_date": self.ordered_date.timestamp(),
            "order_items": [i.get_all(True) for i in self.items],
        }
    
    @classmethod
    def get_orders(cls, status, company_id=None, provider_id=None, per_page=10, page=1):
        # Get orders data and send it in paginated order
        orders_data = []
        
        # If getting orders of a provider
        if not company_id:
            # If status is not selected
            if not status:
                # Get the all the order of the provider
                orders = (
                    db.session.query(Order).filter_by(
                        provider_id=provider_id).order_by(
                        Order.ordered_date.desc()).paginate(
                        per_page=per_page, page=page, error_out=False).items)
                # Append the orders to the list
                orders_data.append([order.get_all(True) for order in orders])
            
            # else, if status is selected
            else:
                # Get the orders of the selected status of the provider
                orders = db.session.query(Order).filter_by(
                    status=status, provider_id=provider_id).order_by(
                    Order.ordered_date.desc()).paginate(
                    per_page=per_page, page=page, error_out=False).items
                if orders:
                    # append the orders to the list
                    orders_data.append([provider.get_all(True) for provider in orders])
            
        # If getting orders of a company
        else:
            # If status is not selected
            if not status:
                # Get the all the order of the company
                orders = (
                    db.session.query(Order).filter_by(
                        company_id=company_id).order_by(
                        Order.ordered_date.desc()).paginate(
                        per_page=per_page, page=page, error_out=False).items)
                # append the orders to the list
                orders_data.append([order.get_all(True) for order in orders])
            # else, if status is selected
            else:
                # Get the orders of the selected status of the company
                orders = db.session.query(Order).filter_by(
                    status=status, company_id=company_id).order_by(
                    Order.ordered_date.desc()).paginate(
                    per_page=per_page, page=page, error_out=False).items
                if orders:
                    # append the orders to the list
                    orders_data.append([provider.get_all(True) for provider in orders])
        
        # Return the orders
        return orders_data


class OrderItem(db.Model):
    __tablename__ = "orderitems"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"))
    product_id = Column(Integer, ForeignKey("products.id"))
    product_quantity = Column(Integer, nullable=False, default=0)
    product = relationship("Product")

    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def get_all(self, short=False):
        if short:
            return {
                "product_id": self.product_id,
                "product_quantity": self.product_quantity,
                "product": self.product.get_all(True),
            }
        return {
            "id": self.id,
            "order_id": self.order_id,
            "product_id": self.product_id,
            "product_quantity": self.product_quantity,
            "product": self.product.get_all(True),
        }


class Customer(db.Model):
    # represent a relationship betn a company and a customer
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    phone_number = Column(String(100), nullable=True)
    email = Column(String(100), nullable=True, unique=True)
    # keep track of when they ordered something, an entry here means some interaction was done
    date = Column(DateTime, default=datetime.utcnow)
    
    def __init__(self, **kwargs):
        user_id = kwargs.get("user_id")
        first_name = kwargs.get("first_name")
        last_name = kwargs.get("last_name")
        phone_number = kwargs.get("phone_number")
        email = kwargs.get("email")
        if not any((user_id, all([first_name, last_name, phone_number, email]))):
            raise ValueError("if no user_id then provide first and last name, phone number and email")
        super().__init__(**kwargs)
    
    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def get_customer_detail(self):
        if not self.user_id:
            return {
                "first_name": self.first_name,
                "last_name": self.last_name,
                "phone_number": self.phone_number,
                "email": self.email,
            }
        user: User = User.query.get(self.user_id)
        return {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "phone_number": user.phone_number,
            "email": user.email,
        }
    
    def get_all(self, short=False):
        customer_detail = self.get_customer_detail()
        if short:
            print(customer_detail)
            return {
                "customer_id": self.id,
                "date": self.date.timestamp(),
                **customer_detail
            }
        return {
            "customer_id": self.id,
            "company_id": self.company_id,
            "date": self.date.timestamp(),
            **customer_detail
        }
    
    # Search for customers by email address, phone number, first name, and last name
    @classmethod
    def get_customers(cls, company_id, needle=None, page=1, per_page=10):
        # If searching customers by name
        if needle:
            # Split the needle
            items_to_search = needle.split(" ")
            # print(items_to_search)
            for item in items_to_search:
                # Search the customers by either first name or last name
                customers = db.session.query(Customer).filter(
                    Customer.first_name.ilike(f"%{item}%") |
                    Customer.last_name.ilike(f"%{item}%") |
                    Customer.phone_number.ilike(f"%{item}%") |
                    Customer.email.ilike(f"%{item}%")).order_by(
                    Customer.date.desc()).paginate(
                    per_page=per_page, page=page, error_out=False).items
                return [customer.get_all(True) for customer in customers]
        
        # Else, return all customers of the company
        else:
            customers = db.session.query(Customer).filter(
                Customer.company_id == company_id).order_by(
                Customer.date.desc()).paginate(
                per_page=per_page, page=page, error_out=False).items
            return [customer.get_all(True) for customer in customers]