from flask import Blueprint, render_template
from src.services.product_service import get_all_products
from src.services.review_service import get_review_stats_for_products


#-------------------UI ROUTES------------------------------

home_bp = Blueprint("home", __name__)
@home_bp.route('/')
@home_bp.route('/home')
def home_page():
    products = get_all_products()
    product_stats = get_review_stats_for_products(products)

    return render_template(
        "home.html",
        products=products,
        product_stats=product_stats
    )
    

contact_bp = Blueprint('contact', __name__)
@contact_bp.route('/contact')
def contact_page():
    return render_template('shop/contact.html')


