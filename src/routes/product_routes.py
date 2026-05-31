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
def admin_product_list():
    return render_template("admin/products/list.html")
    #Diese route ist noch nicht werwendet worden