from flask import render_template, url_for, flash, redirect
from wtforms.validators import Email
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User, Post
from flask_login import login_manager, login_user, current_user, logout_user, login_required

posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018' 
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts, title='Home')


@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
    register_form = RegistrationForm()
    if register_form.validate_on_submit():

        hashed_pass = bcrypt.generate_password_hash(register_form.password.data).decode('utf-8')
        user = User(username=register_form.username.data,
                    password=hashed_pass, 
                    email=register_form.email.data)
        
        db.session.add(user)
        db.session.commit()

        flash(f'Account {register_form.username.data} Registered! You are now able to log In!')
        return redirect(url_for('login'))
    
    return render_template('register.html', title='Register', form=register_form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))


    login_form = LoginForm()
    if login_form.validate_on_submit():
        # checking our data base if the account details is suitable
        user = User.query.filter_by(email=login_form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, login_form.password.data):
            login_user(user, remember=login_form.remember.data)      
            return redirect(url_for('home'))

        flash(f'Login Unsuccessful, Please try Again...')
    
    return render_template('login.html', title='Log in', form=login_form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
     return render_template('account.html', title='Account')
