from os import abort
from flask import render_template, url_for, flash, redirect, request
from wtforms.validators import Email
from flaskblog import app, db, bcrypt
from flaskblog.forms import PostForm, RegistrationForm, LoginForm, UpdateAccountForm
from flaskblog.models import User, Post
from flask_login import login_manager, login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/home")
def home():
    posts = Post.query.all()   
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
            next_page = request.args.get('next')
            # if it is login_required
            return redirect(next_page) if next_page else redirect(url_for('home'))

        flash(f'Login Unsuccessful, Please try Again...')
    
    return render_template('login.html', title='Log in', form=login_form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account", methods=['GET', 'POST'])
# in order to enter it log in required
@login_required
def account(): 
    image_file = url_for('static', filename=f'profile_pics/{current_user.image_file}')
    form = UpdateAccountForm()

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash(f'Account Updated!')
        return redirect(url_for('account'))
        
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    return render_template('account.html', title='Account', profile_pic=image_file, form=form)




@app.route("/post/new", methods=['GET', 'POST'])
# in order to enter it log in required
@login_required
def new_post(): 
  
    form = PostForm()
    
    if form.validate_on_submit():
        title1, content1 = form.title.data, form.content.data  
        post = Post(title=title1, content=content1, author=current_user)
        db.session.commit()
        flash(f'Post Created!')
        return redirect(url_for('home'))

    return render_template('create_post.html', title='New Post', form=form)



@app.route("/post/<int:post_id>", methods=['GET', 'POST'])
@login_required
def post(post_id): 
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)

    if post.author != current_user:
         print("you are not allowed to do this")

    form = PostForm()

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))

    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content

    return render_template('create_post.html', title='Update Post', form=form)


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        print("you are not allowed to do this")

    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))


