from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, Email

class RegistrationForm(FlaskForm):
    
    username = StringField('Username',
     validators=[DataRequired(), Length(min=2, max=20)])

    password = PasswordField('Password',
        validators=[DataRequired()])
    
    confirm_password = PasswordField('Confirm Password',
        validators=[DataRequired(), EqualTo('Password')])
    
    email = StringField('Email',
        validators=[DataRequired(), Email()])
    
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):

    password = PasswordField('Password',
        validators=[DataRequired()])
    
    email = StringField('Email',
        validators=[DataRequired(), Email()])
        
    remember = BooleanField('Remember Me')

    submit = SubmitField('Log In')