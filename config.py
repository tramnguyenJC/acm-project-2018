import os
from itsdangerous import URLSafeTimedSerializer
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'e5ac358c-f0bf-11e5-9e39-d3b532c10a28'
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
		'sqlite:///' + os.path.join(basedir, 'app.db')
	SQUALCHEMY_TRACK_MODIFICATIONS = False
	SERIALIZER = URLSafeTimedSerializer(SECRET_KEY)

	MAIL_SERVER = 'smtp.googlemail.com'
	MAIL_PORT = '587'
	MAIL_USE_TLS = '1'
	MAIL_USERNAME = 'uracm2018@gmail.com'
	MAIL_PASSWORD = 'UR_acm2018'
	ADMINS = ['uracm2018@gmail.com']

	CITIES = [(u'Richmond', u'Richmond'),
		(u'Washington D.C.', u'Washington D.C.'),
		(u'Norfolk', u'Norfolk'),
		(u'Charlottesville', u'Charlottesville')]
	LOCATIONS = [(u'University of Richmond', u'University of Richmond'),
		(u'Richmond International Airport', u'Richmond International Airport'),
		(u'Washington Dulles International Airport', u'Washington Dulles International Airport'),
		(u'Washington Union Station, 50 Massachusetts Ave NE', u'Washington Union Station,  50 Massachusetts Ave NE'),
		(u'EasternShuttle Bus Station, 715 H St NW', u'EasternShuttle Bus Station, 715 H St NW'),
		(u'Smithsonian Metro Station', u'Smithsonian Metro Station'),
		(u'Charlottesville Albemarle Airport (CHO)', u'Charlottesville Albemarle Airport (CHO)'),
		(u'Charlottesville Union Station, 810 W Main St', u'Charlottesville Union Station, 810 W Main St'),
		(u'Greyhound Bus Station, 2910 N Boulevard', u'Greyhound Bus Station, 2910 N Boulevard'),
		(u'Main Street Train Station, 1500 E Main St', u'Main Street Train Station, 1500 E Main St'),
		(u'EasternShuttle Bus Station, 910 N Blvd', u'EasternShuttle Bus Station, 910 N Blvd'),
		(u'Staples Mill Road Station, 7519 Staples Mill Rd', u'Staples Mill Road Station, 7519 Staples Mill Rd'),
		(u'Norfolk Airport (ORF)', u'Norfolk Airport (ORF)')]
	LOCATIONS_BY_CITY = {
		'Richmond': [
			(u'University of Richmond', u'University of Richmond'),
			(u'Richmond International Airport', u'Richmond International Airport'),
			(u'Greyhound Bus Station, 2910 N Boulevard', u'Greyhound Bus Station, 2910 N Boulevard'),
			(u'Main Street Train Station, 1500 E Main St', u'Main Street Train Station, 1500 E Main St'),
			(u'EasternShuttle Bus Station, 910 N Blvd', u'EasternShuttle Bus Station, 910 N Blvd'),
			(u'Staples Mill Road Station, 7519 Staples Mill Rd', u'Staples Mill Road Station, 7519 Staples Mill Rd')],
		'Washington D.C.': [
			(u'Washington Dulles International Airport', u'Washington Dulles International Airport'),
			(u'Washington Union Station, 50 Massachusetts Ave NE', u'Washington Union Station, 50 Massachusetts Ave NE'),
			(u'EasternShuttle Bus Station, 715 H St NW', u'EasternShuttle Bus Station, 715 H St NW'),
			(u'Smithsonian Metro Station', u'Smithsonian Metro Station')],
		'Charlottesville': [
			(u'Charlottesville Albemarle Airport (CHO)', u'Charlottesville Albemarle Airport (CHO)'),
			(u'Charlottesville Union Station, 810 W Main St', u'Charlottesville Union Station, 810 W Main St')],
		'Norfolk': [
			(u'Norfolk Airport (ORF)', u'Norfolk Airport (ORF)')]
	}
