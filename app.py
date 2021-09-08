"""Blogly application."""

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

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

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def delete_user(user_id):
    """Process the page with the deleted user."""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')





