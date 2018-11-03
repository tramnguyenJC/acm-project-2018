from flask import render_template
from flask_mail import Message
from app import app, mail
from threading import Thread

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, text_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    #mail.send(msg)
    Thread(target=send_async_email, args=(app, msg)).start()

def send_request_email(sender_name, sender_contact, sender_message,
                        recipient_username, recipient_email):
    send_email('You Got a Request!',
               sender=app.config['ADMINS'][0],
               recipients=[recipient_email],
               text_body=render_template('email/request_email.txt',
                                          sender_name=sender_name,
                                          sender_contact=sender_contact,
                                          sender_message=sender_message,
                                          recipient_username=recipient_username,
                                          recipient_email=recipient_email))
