from flask import Flask
from app.extensions import db, migrate
from app.main import main
from app.main import models


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # Path to your database file
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Avoids a warning

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Blueprints
    app.register_blueprint(main)

    return app

