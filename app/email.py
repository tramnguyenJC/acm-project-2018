from flask import render_template, url_for
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

def send_confirmation_email(user_email, token, username):
	link = "127.0.0.1:5000/confirm_email/" + token 
	message = render_template('_email_confirmation.html', link=link, username=username)
	send_email("Confirmation Email for UR connect", 
				sender = app.config['ADMINS'][0],
				recipients=[user_email],
				text_body=message)


