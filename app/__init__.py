import os
import secrets

from flask import Flask
from flask_login import LoginManager

from app.routes import init_app
from app.routes.auth import auth_bp
from app.utils.database import close_db
from app.utils.init_db import init_db
from app.models.user import User


def _item_quantity(item):
    """Works whether cart items are dicts or objects."""
    if isinstance(item, dict):
        return int(item.get("quantity") or item.get("Quantity") or 1)
    return int(getattr(item, "quantity", None) or getattr(item, "Quantity", None) or 1)


def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    # Stable key so carts/logins works after restarts (set SECRET_KEY on Render)
    app.secret_key = os.environ.get("SECRET_KEY") or secrets.token_hex(32)
    app.config["DATABASE"] = os.path.join(app.root_path, "northwind.db")

    # Disable template caching during testing
    app.config["TESTING"] = True

    # Initialize database tables
    web_employee_id = init_db(app)
    app.config["WEB_EMPLOYEE_ID"] = web_employee_id

    app.teardown_appcontext(close_db)
    init_app(app=app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    @login_manager.user_loader
    def load_user(user_id):
        return User.get(user_id)

    app.register_blueprint(auth_bp)

    @app.context_processor
    def inject_cart_count():
        count = 0
        try:

            cart = None

            if cart and cart.items:
                count = sum(_item_quantity(i) for i in cart.items)
        except Exception as e:
            app.logger.warning("cart count failed: %s", e)
        return {"cart_count": count}

    return app
