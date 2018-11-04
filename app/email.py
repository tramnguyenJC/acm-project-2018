from flask import render_template
from flask_mail import Message
from app import app, mail

def send_email(subject, sender, recipients, text_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    mail.send(msg)

def send_request_email(email):
    send_email('You Got a Request!',
               sender=app.config['ADMINS'][0],
               recipients=[email],
               text_body=render_template('email/request_email.txt'))
