from flask import Flask
from app.extensions import db, migrate
from app.main import main
from app.main import models
from app.extensions import db, migrate, bcrypt, login_manager


def create_app():
    app = Flask(__name__) # create a flask application instance

    # configure DB
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # set the URI for the SQLite database
    #NOTE URI is used to define the connection string required to access the database
    # sqlite:///app.db is a URI that tells SQLAlchemy to use an SQLite database located in the file app.db
    # the sqlite:// part specifies the database type, and ///app.db specifies the path to the database file

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # disable the feature to track modifications, which avoids a warning
    app.secret_key = "1234"  # key for data decryption

    # Initialize extensions
    db.init_app(app) # bind the SQLAlchemy instance to the Flask app
    migrate.init_app(app, db) # bind the Migrate instance to the Flask app and the database instance

    # initialize bcrypt and login_manager
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # protect some urls unless user is login
    login_manager.login_view = "main.register_login"


    # Blueprints
    app.register_blueprint(main)

    return app

