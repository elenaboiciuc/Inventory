from app.extensions import db, login_manager
from flask_login import UserMixin


class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    number = db.Column(db.Integer, unique=True, nullable=False)
    description = db.Column(db.String(100), unique=True, nullable=False)
    registration_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(30), nullable=False)
    booked = db.Column(db.String(10), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=True)

class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key = True)
    user_name = db.Column(db.String(80), unique=True, nullable=False)
    user_email = db.Column(db.String(80), unique=True, nullable=False)
    user_password = db.Column(db.String(80), unique=False, nullable=False)
    items = db.relationship('Inventory', backref='owner', lazy=True)  # establishes a one-to-many relationship with Inventory (one user can own many items)

    def get_id(self):
        return self.user_id # retrieves the user's ID for user loading functionality

# function to load a user based on user_id, used by Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) # query the database to retrieve the user instance corresponding to the user_id





