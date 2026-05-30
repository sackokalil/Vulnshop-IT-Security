from flask import Flask
from src.routes.landing_pages_routes import admin_dash_bp, home_bp, contact_bp, cart_bp
from src.routes.product_routes import product_bp



def create_app():
    app = Flask(__name__)
    app.config.from_object("src.config.config.Config")

    app.register_blueprint(admin_dash_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(contact_bp)
    app.register_blueprint(cart_bp)

    return  app