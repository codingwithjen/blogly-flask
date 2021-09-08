"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMG_URL = "https://tpng.net/download/800x800_175-1757519_starwars-png.png"

class User(db.Model):
    """User."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable=False, default=DEFAULT_IMG_URL)

    @property
    def full_name(self):
        """Return the full name of the user."""

        return f"{self.first_name} {self.last_name}"

### Setup of SQLAlchemy and calling it into your Flask app

def connect_db(app):
    """Connect this database for Flask app."""

    db.app = app
    db.init_app(app)




