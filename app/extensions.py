from flask_migrate import Migrate # for database migrations
from flask_sqlalchemy import SQLAlchemy # for database interaction
from flask_bcrypt import Bcrypt # for hashing passwords
from flask_login import LoginManager # for managing user sessions

# declaration of DB and Migrate
db = SQLAlchemy()
migrate = Migrate()

# declaration of Bcrypt and LoginManager
bcrypt = Bcrypt() #  pass management for a registered user
login_manager = LoginManager()  # this will handle the user login/logout operations

