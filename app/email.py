from flask import render_template
from flask_mail import Message
from app import app, mail
from threading import Thread

def send_email(subject, sender, recipients, text_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    Thread(target=send_async_email, args=(app, msg)).start()

def send_request_email(email):
    send_email('You Got a Request!',
               sender=app.config['ADMINS'][0],
               recipients=[email],
               text_body=render_template('email/request_email.txt'))

def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email('[UR Connect] Reset Your Password',
               sender=app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt',
                                         user=user, token=token))

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)
