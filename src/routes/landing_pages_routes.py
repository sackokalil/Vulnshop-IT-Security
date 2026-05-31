from flask import Blueprint
from flask import render_template

admin_dash_bp = Blueprint("admin", __name__, url_prefix="/admin")

#-------------------Admin landing page--------------------

@admin_dash_bp.route("/dashboard")
def dashboard():
    return render_template("admin/index.html")


#-------------------UI ROUTES------------------------------

home_bp = Blueprint("home", __name__)
@home_bp.route('/')
@home_bp.route('/home')
def home_page():
    return render_template('home.html')


contact_bp = Blueprint('contact', __name__)
@contact_bp.route('/contact')
def contact_page():
    return render_template('shop/contact.html')

cart_bp = Blueprint('cart', __name__)
@cart_bp.route('/cart')
def cart_page():
    return render_template('shop/cart.html')