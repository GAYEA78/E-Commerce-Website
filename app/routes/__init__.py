from flask import Flask

from app.routes.main import main_bp
from app.routes.product import product_bp
from app.routes.status import status_bp


def init_app(app: Flask):
    """Initialize all blueprints with the app"""
    app.register_blueprint(main_bp)
    app.register_blueprint(status_bp, url_prefix="/status")
    app.register_blueprint(product_bp, url_prefix="/product")
