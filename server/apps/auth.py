from server.db.models import User
from server.tools.mail_sender import send_email_verification
from werkzeug.exceptions import HTTPException
from flask_jwt_extended import (JWTManager as JWTManager,
                                create_access_token,create_refresh_token,
                                get_jwt_identity,
                                jwt_required, current_user
                                )
from flask import Flask, request, make_response, abort, g
import logging
from functools import wraps
from server.apps.errorhandlers import init_jwt_errorhandlers


def get_current_employee(user_id):
    pass



def init_rest_api_authentication(app):
    # This function is connected to app


    jwt = JWTManager(app)

    @jwt.user_identity_loader
    def jwt_payload_user_identity_lookup(user):
        return user

    @jwt.user_lookup_loader
    def jwt_payload_user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.query.filter_by(id=identity).one_or_none()


    init_jwt_errorhandlers(jwt)


