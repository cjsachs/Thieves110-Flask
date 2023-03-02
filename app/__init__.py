from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# INITIALIZING SECTION
app = Flask(__name__)
app.config.from_object(Config)

# Register Packages
login = LoginManager(app)

# Database Manager
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Configure Settings
login.login_view = 'login'
login.login_message = 'You must log in to access this page.'
login.login_message_category = 'warning'


from app import routes