from flask import Flask
from src.routes.landing_pages_routes import admin_dash_bp, home_bp, contact_bp, cart_bp
from src.routes.product_routes import product_bp, admin_product_bp
from src.routes.auth_routes import login_bp, register_bp
from src.routes.order_routes import admin_order_bp

from src.routes.vulnerability_routes import vulnerability_bp
from src.routes.user_routes import user_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object("src.config.config.Config")

    app.register_blueprint(admin_dash_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(contact_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(register_bp)

    app.register_blueprint(admin_product_bp)
    app.register_blueprint(admin_order_bp)

    app.register_blueprint(vulnerability_bp)

    app.register_blueprint(user_bp)


    return  app