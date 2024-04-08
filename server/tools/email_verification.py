from flask import current_app
import random
from itsdangerous import URLSafeTimedSerializer
import pytz
import random
import string
import datetime
import jwt



def generate_email_verification_token(data : dict):
    code = random.randint(100_000, 999_999)
    expiration = datetime.datetime.utcnow().timestamp() + 60*60
    dt = {
        'data': {
            'code': code,
            'expiration': expiration
        },
        'user': data
    }
    token = jwt.encode(dt, current_app.config['SECRET_KEY'])
    return code, token


def confirm_email_verification_token(token : str, code : int):
    try:
        dt = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
    except:
        return None, "Failed decoding the token"
    try:
        if datetime.datetime.utcnow().timestamp() - dt['data']['expiration'] > 60*60:
            raise ValueError("Token has exprired")
        if dt['data']['code'] != int(code):
            raise ValueError("Wrong code")
    except ValueError as e:
        return None, str(e)
    return dt['user'], None


