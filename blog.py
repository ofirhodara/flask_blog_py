from datetime import timedelta
from flask import Flask, render_template, url_for
from flask_wtf import form
from forms import RegistrationForm, LoginForm
app = Flask(__name__)


app.config['SECRET_KEY'] = '2002ofirhodaraSecretKey2002'

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


@app.route("/login")
def register():
    register_form = RegistrationForm()
    return render_template('register.html', title='Register', form=register_form)


@app.route("/register")
def login():
    login_form = LoginForm()
    return render_template('login.html', title='Log in', form=login_form)


if __name__ == '__main__':
    app.run(debug=True)