from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity, \
                               unset_jwt_cookies, jwt_required, JWTManager, create_refresh_token, current_user
from flask_restful import Resource
from ..api import api_response
from server.db.models import User, Company
from flask import abort, request, current_app
from server.tools.email_verification import confirm_email_verification_token, generate_email_verification_token
import datetime
from server.mailserver import FlaskMailServer
from werkzeug.exceptions import Unauthorized, Conflict
from config import ApplicationConfig
from ..app import db


class SendEmailVerificationCode(Resource):
    def post(self):
            data = request.get_json()

            globals().update(data)

            if not all((email, phone_number, password, first_name, last_name)): # pyright: ignore
                abort(400, "Some required fields are empty.")
            user : User = User.query.filter_by(email=email).first() # pyright: ignore
            
            if user: raise Conflict
            
            code, token = generate_email_verification_token(data) # pyright: ignore
            mail = FlaskMailServer(current_app)
            mail.send_email_confirmation_of_email([email], code) # pyright: ignore

            return api_response({
                "token": token
            }, description="Email verification sent to {}".format(email)) # pyright: ignore


class ConfirmEmailVerificationCode(Resource):
    def post(self):
        code = request.get_json().get("code")
        token = request.get_json().get("token")
        if not all((code, token)):
            abort(400, "Fields missed")
       
        data, error = confirm_email_verification_token(token, code)
        if error: abort(400, error)
        user = User(**data)
        user.is_active = True
        user.confirmed_on = datetime.datetime.utcnow()
        user.insert()
        return api_response(user.get_all(), "Email has been confirmed successfully")


class SignupResource(Resource):
    def post(self):
        # Get the input data from the request
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        name = data.get('name')

        # Check if the email is already registered
        if User.query.filter_by(email=email).first():
            raise Conflict("Email address already registered")
        # Create a new user with the input data
        new_user = User(email=email, name=name)
        new_user.set_password(password)

        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        # Generate access and refresh tokens for the new user
        access_token = create_access_token(identity=new_user.id)
        refresh_token = create_refresh_token(identity=new_user.id)

        # Return the tokens in the response
        return api_response({
            "access_token": access_token,
            "refresh_token": refresh_token
            }, "You Signed Up successfully")


class LoginResource(Resource):
    def post(self):
        
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        remember_me = data.get('remember_me', False)

        # db_user : User = User.query.filter_by(email=email, is_active=True).first()
        db_user : User = User.query.filter_by(email=email).first()
        if not db_user:
            raise Unauthorized
        if not db_user.verify_password(password):
            raise Unauthorized
        
        access_token = create_access_token(identity=db_user.id)
        refresh_token = create_refresh_token(identity=db_user.id,
                    expires_delta=
                    ApplicationConfig.JWT_REFRESH_TOKEN_EXPIRES_WHEN_REMEMBER
                    if remember_me else
                    ApplicationConfig.JWT_REFRESH_TOKEN_EXPIRES)

        return api_response({
            "access_token": access_token,
            "refresh_token": refresh_token
            }, "Logged in successfully")



class CreateCompanyResource(Resource):
    @jwt_required()
    def post(self):
            data = request.get_json()
            
            name_in_law = data.get('name_in_law')
            name = data.get('name')
            login = data.get('login')
            email = data.get('email')
            phone_number = data.get('phone_number')

            user_company = Company.query.filter_by(email=email).first()
            if user_company:
                raise Conflict("Email exists")
            user_company = Company.query.filter_by(phone_number=phone_number).first()
            if user_company:
                raise Conflict("Phone number exists")
            user_company = Company.query.filter_by(login=login).first()
            if user_company:
                raise Conflict("Login exists")
            try:
                new_company = Company(
                    email=email,
                    name_in_law=name_in_law,
                    name=name,
                    login=login,
                    phone_number=phone_number,
                    owner_id=current_user.id
                )
                new_company.insert()
            except:
                abort(400, "Fields missing")
            # redirect user to verification email page
            # send_email_verification(mail, email )
            return api_response(new_company.get_all(), "Created successfully", 201)
        