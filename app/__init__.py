import os
import secrets

from flask import Flask
from flask_login import LoginManager

from app.routes import init_app
from app.routes.auth import auth_bp
from app.utils.database import close_db
from app.utils.init_db import init_db
from app.models.user import User  # You'll need to create this


def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    secret_key = secrets.token_hex(32)
    app.secret_key = secret_key
    app.config["DATABASE"] = os.path.join(app.root_path, "northwind.db")

    # Disable template caching during testing
    app.config["TESTING"] = True

    # Initialize database tables
    web_employee_id = init_db(app)
    app.config["WEB_EMPLOYEE_ID"] = web_employee_id

    app.teardown_appcontext(close_db)
    init_app(app=app)

    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.get(user_id)  # Implement this method in your User model

    # Register auth blueprint
    app.register_blueprint(auth_bp)

    return app
