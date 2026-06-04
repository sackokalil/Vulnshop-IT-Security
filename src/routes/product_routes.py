from flask import Blueprint, render_template

from src.services.product_service import (
    get_all_products,
    get_product_by_id
)

product_bp = Blueprint(
    'product',
    __name__,
    url_prefix='/products'
)



@product_bp.route('/')
def product_list():

    products = get_all_products()

    return render_template(
        "shop/index.html",
        products=products
    )


@product_bp.route('/<int:product_id>')
def detail_product(product_id):

    product = get_product_by_id(product_id)

    return render_template(
        "shop/product.html",
        product=product
    )





#-----------------------------------Admin part----------------------------------------------

admin_product_bp = Blueprint("admin_product", __name__, url_prefix="/admin/products")


@admin_product_bp.route("/")
def product_list():
    return render_template("admin/products/products.html")
    #Diese route ist noch nicht werwendet worden


@admin_product_bp.route("/add_product")
def add_product_form():
    return render_template("admin/products/add_product.html")

@admin_product_bp.route('/add_category')
def add_category_form():
    return render_template('admin/categories/add_categorie_form.html')

@admin_product_bp.route('/categories')
def category_list():
    return render_template('admin/categories/categories.html')