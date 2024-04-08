from datetime import datetime

from flask_jwt_extended import create_access_token, jwt_required, current_user
from flask_restful import Resource
from ..api import api_response
from flask import abort, request, current_app
from threading import Timer
from ...db.models import User, Notification
from sqlalchemy.orm import joinedload

class ProfileEditResource(Resource):
    @jwt_required()
    def put(self):
        try:
            data = request.get_json()
            user = User.query.get(current_user.id)
            if data:
                for key, value in data.items():
                    if key in ["avatar", "email", "first_name", "last_name", "phone_number"]:
                        setattr(user, key, value)
                        user.update()

                return api_response(user.get_all(), "Profile edited")
            else:
                return abort(400, "Invalid data fields or no any data")
        except:
            abort(400)


class ProfileUpdateStatusResource(Resource):
    @jwt_required()
    def put(self):
        # Get User
        user = User.query.get(current_user.id)
        # Update last_online_date
        user.last_online_date = datetime.utcnow()
        # Update user in table
        user.update()
        
        nots = Notification.get_unread_nots(current_user.id)

        # Return response
        return api_response(description="User Online Status updated", result={"nots": nots})

