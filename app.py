"""Blogly application."""

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

## print all SQL statements to the terminal (helpful for debugging)
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "oh-so-secret"

## if you want to turn off the debug toolbar uncomment line below:
## app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

### Routes

@app.route('/')
def start():
    """Homepage that redirects to list of users."""

# Flask tools redirecting
    return redirect('/users')

### Show all the users. Make these links to view the detail page for the user. Have a link here to the add-user form

@app.route('/users')
def index():
    """Show all users on the index page."""

    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users/index.html', users=users)

### Switches from GET to POST to get user information

@app.route('/users/new',methods=['GET'])
def add_user_form():
    """Show a form to add users."""

    return render_template('users/new.html')

@app.route('/users/new', methods=['POST'])
def new_users():
    """Process the add form, adding a new user and going back to /users."""

    new_user = User(
        first_name = request.form['first_name'],
        last_name = request.form['last_name'],
        image_url = request.form['image_url'] or None)

    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

### Show information about the given user. Have a button to get to their edit page, and to delete the user

@app.route('/users/<int:user_id>')
def show_users(user_id):
    """Show information about the given user."""

    user = User.query.get_or_404(user_id)
    return render_template('users/show.html', user=user)

### Show the edit page for a user. Hae a cancel button that returns to the detail page for a user, and save a button that updates that user

@app.route('/users/<int:user_id>/edit')
def edit_users(user_id):
    """Show the edit page for a user."""

    user = User.query.get_or_404(user_id)
    return render_template('users/edit.html', user=user)

### Process the edit form, returning the user to the /users page

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def update_user(user_id):
    """Process the edit form, and return the user to the /users page."""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect('/users')

### Remove the user due to deletion

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Process the page with the deleted user."""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')


### Posts Routes

@app.route('/users/<int:user_id>/posts/new')
def new_form_posts(user_id):
    """Show form to add a post for that user."""

    user = User.query.get_or_404(user_id)
    return render_template('posts/new.html', user=user)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def new_posts(user_id):
    """Handle add form; add post and redirect to the user detail page."""

    user = User.query.get_or_404(user_id)
    new_post = Post(title = request.form['title'],
                    content = request.form['content'], user=user)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/users/{ user_id }")

### Show a post and show buttons to edit and delete the post

@app.route('/posts/<int:post_id>')
def show_posts(post_id):
    """Show a post."""

    post = Post.query.get_or_404(post_id)
    return render_template('posts/show.html', post=post)

### Show form to edit a post and to cancel (back to user page)

@app.route('/posts/<int:post_id>/edit')
def edit_posts(post_id):
    """Show form to edit a post."""

    post = Post.query.get_or_404(post_id)
    return render_template('posts/edit.html', post=post)

### Handle form submission of a post. Redirect back to the post view

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def updated_posts(post_id):
    """Handle editing of a post."""

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()

    return redirect(f"/users/{post.user_id}")

### Deletion

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    """Delete the post."""

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{ post.user_id }')





