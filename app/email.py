from flask import render_template, url_for
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

def send_request_email(sender_name, sender_contact1, sender_contact2, sender_message,
                        recipient_username, recipient_email, origin, destination, date):
    send_email('You Got a Request!',
               sender=app.config['ADMINS'][0],
               recipients=[recipient_email],
               text_body=render_template('email/request_email.txt',
                                          sender_name=sender_name,
                                          sender_contact1=sender_contact1,
                                          sender_contact2=sender_contact2,
                                          sender_message=sender_message,
                                          recipient_username=recipient_username,
                                          recipient_email=recipient_email,
                                          origin=origin,
                                          destination=destination,
                                          date=date))


def send_confirmation_email(user_email, token, username):
  link = "127.0.0.1:5000/confirm_email/" + token 
  message = render_template('_email_confirmation.html', link=link, username=username)
  send_email("Confirmation Email for UR connect", 
        sender = app.config['ADMINS'][0],
        recipients=[user_email],
        text_body=message)

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
