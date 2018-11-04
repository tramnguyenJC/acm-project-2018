from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
from datetime import time
from datetime import datetime
from flask_login import UserMixin
from app import db
from app import login

class User(UserMixin, db.Model):
	id 				= db.Column(db.Integer, primary_key = True)
	username 		= db.Column(db.String(64), index=True, unique=True)
	email 			= db.Column(db.String(120), index=True, unique=True)
	password_hash 	= db.Column(db.String(128))
	requests 		= db.relationship('Request', backref='author', lazy='dynamic')

	def __repr__(self):
		return '<User {}>'.format(self.username)

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

class Request(db.Model):
	id 					= db.Column(db.Integer, primary_key = True)
	origin_city 		= db.Column(db.String(140))
	origin 				= db.Column(db.String(140))
	destination_city 	= db.Column(db.String(140))
	destination 		= db.Column(db.String(140))
	date 				= db.Column(db.Date, index = True)
	time 				= db.Column(db.Time, index = True)
	user_id 			= db.Column(db.Integer, db.ForeignKey('user.id'))
	description 		= db.Column(db.String(140))
	def __repr__(self):
		return '<Request {}>'.format(self.destination)


@login.user_loader
def load_user(id):
	return User.query.get(int(id))
