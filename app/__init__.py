from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from config import Config
from flask_talisman import Talisman
from flask_fontawesome import FontAwesome
from flask_mail import Mail

app = Flask(__name__)

fa = FontAwesome(app)
talisman = Talisman(
    app,
    content_security_policy={
        'default-src': "'self'",
        'img-src': [
        	'*',
        ],
        'script-src': [
            "'self'",
            'cdnjs.cloudflare.com',
            'maxcdn.bootstrapcdn.com',
            'ajax.googleapis.com',
        ],
        'style-src': [
            "'self'",
            'maxcdn.bootstrapcdn.com',
            'cdnjs.cloudflare.com',
        ],
    },
    content_security_policy_nonce_in=['script-src'], 
)

app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login = LoginManager(app)
login.login_view = 'login'

bootstrap = Bootstrap(app)
mail = Mail(app)


from app import routes, models
