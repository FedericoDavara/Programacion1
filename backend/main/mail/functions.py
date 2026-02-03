from .. import mailsender #el que cree en el init
from flask import current_app, render_template
from flask_mail import Message
from smtplib import SMTPException #Viene con flask
from jinja2 import TemplateNotFound

#La funcion pide al menos 3 atributos: to a quien envio, subjet asunto del mail y el template 
def sendMail(to, subject, template, **kwargs):
    #Configuracion del mail
    msg = Message( subject, sender=current_app.config['FLASKY_MAIL_SENDER'], recipients=to)
    try:
        #Creación del cuerpo del mensaje
        msg.body = render_template(template + '.txt', **kwargs)
        msg.html = render_template(template + '.html', **kwargs)
        #Envío de mail
        result = mailsender.send(msg)
    except (SMTPException, TemplateNotFound) as e:
        # Log the error and return False so callers can decide how to proceed
        print(f"Mail send error: {e}")
        return False
    except Exception as e:
        # Catch-all to avoid unhandled exceptions (e.g., rendering issues)
        print(f"Unexpected error sending mail: {e}")
        return False
    return True