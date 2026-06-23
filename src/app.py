from flask import Flask
from src.routes.landing_pages_routes import  home_bp, contact_bp
from src.routes.dashboard_routes import admin_dash_bp
from src.routes.product_routes import product_bp, admin_product_bp
from src.routes.auth_routes import login_bp, register_bp, logout_bp, forgot_password_bp
from src.routes.order_routes import admin_order_bp, order_bp
from src.routes.profile_route import profile_bp
from src.routes.category_route import admin_category_bp
from src.routes.cart_routes import cart_bp
from src.routes.review_routes import review_bp

from src.routes.user_routes import admin_user_bp

from src.routes.vulnerabilities_routes import (
    admin_vulnerability_bp
)



def create_app():
    app = Flask(__name__)
    app.config.from_object("src.config.config.Config")
    app.secret_key = "vulnshop-dev-secret-key"

    app.register_blueprint(admin_dash_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(contact_bp)
   
    app.register_blueprint(login_bp)
    app.register_blueprint(logout_bp)
    app.register_blueprint(register_bp)
    app.register_blueprint(forgot_password_bp)

    app.register_blueprint(admin_product_bp)
    app.register_blueprint(admin_category_bp)

    app.register_blueprint(cart_bp)

    app.register_blueprint(admin_order_bp)
    app.register_blueprint(order_bp)

    app.register_blueprint(profile_bp)

    app.register_blueprint(review_bp)

   

    app.register_blueprint(admin_user_bp)


    app.register_blueprint(admin_vulnerability_bp)



    return  app