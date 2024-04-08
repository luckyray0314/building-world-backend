
from flask_mail import Mail, Message



class FlaskMailServer(Mail):
    # NO CHANGING
    def send_email(self, subject : str = '', recipients = None, template_path : str = None, variables : dict = None):
        msg = Message(subject, sender=self.app.config['MAIL_DEFAULT_SENDER'], recipients=recipients)
        msg.html = ''
        if template_path:
            with open(template_path,'r') as f:
                msg.html = f.read().format(**variables)
        self.send(msg)
    
    # ---------------------------------------------
    # continue sending custom emails

    def send_email_confirmation_of_email(self, recipients, code):
        return self.send_email("PLease confirm your email address", recipients,
                                "server/templates/emails/email_confirmation.html", { "code": code })
    
    def send_email_invitation_to_company(self, recipients, button_link):
        return self.send_email("Invitation letter", recipients,
                                "server/templates/emails/invitation_to_the_company.html", { "button_link": button_link })


    
