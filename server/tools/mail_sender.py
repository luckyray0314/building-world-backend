

from flask import request
from flask_mail import Message


def send_email_verification(mail, to,  token):
    subject = "Confirm your email address"
    template = 'Error. [[[button_link]]]'
    """
    *****************************************************
    """
    try:
        with open("example.html","r",encoding="utf8") as w:
            template = w.read()
    except: pass
    button_url = request.host_url + "confirm-email/" + token
    template = template.replace("[[[button_link]]]", button_url)

    msg = Message(
        subject,
        recipients=[to],
        html=template
    )
    mail.send(msg)
