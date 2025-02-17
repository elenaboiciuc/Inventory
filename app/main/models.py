from app import db


class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    description = db.Column(db.String(100), unique=True, nullable=False)
    registration_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(30), nullable=False)
    booked = db.Column(db.String(10), nullable=False)

