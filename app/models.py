from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
from datetime import time
from datetime import datetime
from flask_login import UserMixin
from app import db
from time import time
from app import login
import jwt
from app import app

class User(UserMixin, db.Model):
	id 				= db.Column(db.Integer, primary_key = True)
	username 		= db.Column(db.String(64), index=True, unique=True)
	email 			= db.Column(db.String(120), index=True, unique=True)
	password_hash 	= db.Column(db.String(128))
	posts 			= db.relationship('Post', backref='author', lazy='dynamic')
	requests 		= db.relationship('Request', backref='author', lazy='dynamic')

	def __repr__(self):
		return '<User {}>'.format(self.username)

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

	def get_reset_password_token(self, expires_in=600):
		return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

	@staticmethod
	def verify_reset_password_token(token):
		try:
			id = jwt.decode(token, app.config['SECRET_KEY'],
				algorithms=['HS256'])['reset_password']
		except:
			return

		return User.query.get(id)

class Post(db.Model):
	id 			= db.Column(db.Integer, primary_key = True)
	body 		= db.Column(db.String(140))
	timestamp 	= db.Column(db.DateTime, index=True, default=datetime.utcnow)
	user_id 	= db.Column(db.Integer, db.ForeignKey('user.id'))
	def __repr__(self):
		return '<Post {}>'.format(self.body)


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
