from flask import Flask, jsonify, session
import random
from itsdangerous import URLSafeTimedSerializer

import random
import string
import datetime


def generate_otp():
    """Generates a random OTP consisting of 6 digits"""
    return ''.join(random.choices(string.digits, k=6))


def generate_otp_token(email):
    """Generates an OTP token and stores it in the Flask session for confirmation"""
    token = generate_otp()
    expiration = datetime.datetime.now() + datetime.timedelta(minutes=5)
    session['otp_token'] = token
    session['otp_expiration'] = expiration
    session['otp_email'] = email
    return token


def confirm_otp_token(token):
    """Confirms an OTP token and returns the associated email address"""
    try:
        if 'otp_token' not in session or 'otp_expiration' not in session or 'otp_email' not in session:
            raise ValueError('Session data not available')
        if session['otp_token'] != token or datetime.datetime.now() > session['otp_expiration']:
            raise ValueError('Invalid OTP token')
    except ValueError as e:
        return None, str(e)
    return session['otp_email'], None


# def generate_token():
#     from server.apps.app import app
#     serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
#     otp = str(random.randint(10000, 99999))

#     token = serializer.dumps({'otp': otp}).decode('utf-8')

#     # return the token
#     return jsonify({
#         'token': token
#     })


# def confirm_token(token, expiration=3600):
#     from server.apps.app import app
#     serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
#     try:
#         email = serializer.loads(
#             token,
#             max_age=expiration
#         )
#     except:
#         return jsonify({
#             'valid': False
#         })

#     # the data variable will contain the original data that was signed, in this case the OTP
#     otp = email['otp']

#     # return the OTP
#     return jsonify({
#         'valid': True,
#         'otp': otp
#     })
