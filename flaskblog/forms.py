from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username',
     validators=[DataRequired(), Length(min=2, max=20)])

    password = PasswordField('Password',
        validators=[DataRequired()])
    
    confirm_password = PasswordField('Confirm Password',
        validators=[DataRequired(), EqualTo('password', "Password's must match")])
    
    email = StringField('Email',
        validators=[DataRequired(), Email()])
    
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(f'User {username.data} user name is already exists')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(f'User {email.data} email is already exists')

class LoginForm(FlaskForm):

    password = PasswordField('Password',
        validators=[DataRequired()])
    
    email = StringField('Email',
        validators=[DataRequired()])
        
    remember = BooleanField('Remember Me')

    submit = SubmitField('Log In')