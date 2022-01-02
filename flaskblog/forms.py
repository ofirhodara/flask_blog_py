from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User
from flask_login import current_user


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


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
     validators=[DataRequired(), Length(min=2, max=20)])

    email = StringField('Email',
        validators=[DataRequired(), Email()])


    submit = SubmitField('Update')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if current_user.username != username.data:
            if user:
                raise ValidationError(f'User {username.data} user name is already exists')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if current_user.email != email.data:
            if user:
                raise ValidationError(f'User {email.data} email is already exists')



class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')