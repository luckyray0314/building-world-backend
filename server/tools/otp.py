import math, random
from flask import request




import secrets

# otp = random.randint(00000, 99999)


# def generate_token(length):
#     """ Generates an alphanumerical token for the specified length"""
#     return secrets.token_hex(length)

       
def confirm_otp(otp):
    from server.apps.api import api_response
    data =  request.get_json()
    user_otp = data.get("otp")
    if otp == int(user_otp):
        return api_response({
            'otp': user_otp,
            "Verification Email": "Email Verified Successfully"
            })
    else:
        return api_response({
                "Error": "email can't be verified"
            })