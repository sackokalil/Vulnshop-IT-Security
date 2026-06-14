from flask import Blueprint, render_template, url_for, flash, redirect, request
from src.services.category_service import get_all_categories

from src.services.product_service import (
    get_all_products,
    get_product_by_id,
    create_product,
    edit_product,
    remove_product
)
from src.services.review_service import (
    get_reviews_by_product_id,
    get_review_stats_by_product_id
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
    reviews = get_reviews_by_product_id(product_id)
    review_stats = get_review_stats_by_product_id(product_id)

    return render_template(
        "shop/product.html",
        product=product,
        reviews=reviews,
        review_stats=review_stats
    )





#-----------------------------------Admin part----------------------------------------------

admin_product_bp = Blueprint("admin_product", __name__, url_prefix="/admin/products")


@admin_product_bp.route("/")
def admin_product_list():
    products = get_all_products()

    return render_template(
        "admin/products/products.html",
        products=products
    )
    


@admin_product_bp.route("/add_product", methods=["GET", "POST"])
def add_product_form():

    categories = get_all_categories()

    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        price = request.form.get("price")
        category = request.form.get("category")
        image_url = request.form.get("image_url")

        create_product(name, description, price, category, image_url)

        flash("Product added successfully!", "success")

        return redirect(url_for("admin_product.add_product_form"))

    return render_template(
        "admin/products/add_product.html",
        categories=categories
    )

@admin_product_bp.route("/<int:product_id>/edit", methods=["GET", "POST"])
def edit_product_form(product_id):

    product = get_product_by_id(product_id)
    categories = get_all_categories()

    if not product:
        flash("Product not found.", "danger")
        return redirect(url_for("admin_product.admin_product_list"))

    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        price = request.form.get("price")
        category = request.form.get("category")
        image_url = request.form.get("image_url")

        edit_product(
            product_id=product_id,
            name=name,
            description=description,
            price=price,
            category=category,
            image_url=image_url
        )

        flash("Product updated successfully!", "success")
        return redirect(url_for("admin_product.admin_product_list"))

    return render_template(
        "admin/products/edit_product.html",
        product=product,
        categories=categories
    )


@admin_product_bp.route("/<int:product_id>/delete")
def delete_product(product_id):

    product = get_product_by_id(product_id)

    if not product:
        flash("Product not found.", "danger")
        return redirect(url_for("admin_product.admin_product_list"))

    remove_product(product_id)

    flash("Product deleted successfully!", "success")
    return redirect(url_for("admin_product.admin_product_list"))