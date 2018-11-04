from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, DateField, SelectField
from wtforms_components import TimeField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User, Request
from app import app
from flask_bootstrap import Bootstrap

class LoginForm(FlaskForm):
    username    = StringField('Username',           validators=[DataRequired()])
    password    = PasswordField('Password',         validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit      = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username    = StringField('Username',           validators=[DataRequired()])
    email       = StringField('Email',              validators=[DataRequired(), Email()])
    password    = PasswordField('Password',         validators=[DataRequired()])
    password2   = PasswordField('Repeat Password',  validators=[DataRequired(), EqualTo('password')])
    submit      = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class PostForm(FlaskForm):
    post    = TextAreaField('Say something',
            validators  = [DataRequired(), Length(min=1, max=140)])
    submit  = SubmitField('Submit')

class RequestForm(FlaskForm):
    origin_city = SelectField(u'Which city are you traveling from?',
            validators  = [DataRequired()], id='select_origin_city')

    origin = SelectField(u'Which location you traveling from?',
            validators  = [DataRequired()], id='select_origin')

    destination_city = SelectField(u'Which city are you traveling to?',
            validators  = [DataRequired()], id='select_destination_city')

    destination = SelectField(u'Which location are you traveling to?',
            validators  = [DataRequired()], id='select_destination')

    date = DateField(u'What date are you traveling?',
            validators = [DataRequired()],
            id='datepick',
            render_kw={"placeholder": "MM/DD/YY"},
            format='%m/%d/%y')
                            
    time = TimeField('When are you traveling? (Please give a tentative time)',
            validators = [DataRequired()],
            id='timepick',
            format='%I:%M %p')

    description = TextAreaField('Optional Description')
    submit      = SubmitField('Submit')

class SearchForm(FlaskForm):
    origin      = SelectField('Going From', validators = [DataRequired()])
    destination = SelectField('To',         validators = [DataRequired()])

    date = DateField('Traveling On ',
            validators = [DataRequired()],
            render_kw   = {"placeholder": "MM/DD/YY"},
            format      = "%m/%d/%y",
            id          = 'datepicker')

    search = SubmitField('Search')

class EmailContentForm(FlaskForm):
    name = StringField('Your Name (required)', validators=[DataRequired()])
    contact1 = StringField('Primary Contact (required)', validators=[DataRequired()])
    contact2 = StringField('Secondary Contact (optional)')
    message = TextAreaField('More Information You Want to Provide (optional)')
    submit = SubmitField('Submit')
