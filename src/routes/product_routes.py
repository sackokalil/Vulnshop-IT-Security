from flask import Blueprint, render_template, url_for, flash, redirect, request, current_app
from src.services.category_service import get_all_categories
import os
from werkzeug.utils import secure_filename
from src.services.security_event_service import create_security_event



from src.services.product_service import (
    get_all_products,
    get_product_by_id,
    create_product,
    edit_product,
    remove_product,
    search_products
)
from src.services.review_service import (
    get_reviews_by_product_id,
    get_review_stats_by_product_id,
    get_review_stats_for_products
)




product_bp = Blueprint(
    'product',
    __name__,
    url_prefix='/products'
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

#---------------------------------------------------

def contains_union_sql_payload(value):
    if not value:
        return False

    value = value.lower()

    suspicious_patterns = [
        "union select",
        "' union",
        "--",
        " from users",
        "from"
        "password",
        "sqlite_master"
    ]

    for pattern in suspicious_patterns:
        if pattern in value:
            return True

    return False


@product_bp.route("/search")
def search_product():
     # This endpoint is intentionally vulnerable to:
    # 1. Reflected XSS: search_query is rendered with |safe in home.html:
    # The value of "query" comes directly from the URL.
    # Example:
    # /products/search?query=<script>alert('Reflected XSS')</script>
    # The value is not stored in the database.
    # It is only reflected back into the HTML response.
    # The vulnerability becomes active if the template renders it with "|safe".

    # 2. Union-Based SQL Injection: search query is used unsafely in product search
    #3. Blind sql injection : 1 OR 1=1 ; 

    #the three search vulnerabilities are implemented in the file product.py in the function
    #search_products_by_keyword(keyword); which is called by the function bellow
    #search_products(query) implemented in the file product_service.py
    

    query = request.args.get("query", "").strip()

    if contains_union_sql_payload(query):
        create_security_event(
            event_type="UNION_SQL_INJECTION_ATTEMPT",
            severity="High",
            description="Union-Based SQL Injection payload submitted in product search.",
            user_id=None,
            endpoint=request.path,
            ip_address=request.remote_addr,
            user_agent=request.headers.get("User-Agent")
        )

    products = search_products(query)

    product_stats = get_review_stats_for_products(products)

    return render_template(
        "home.html",
        products=products,
        product_stats=product_stats,
        search_query=query
    )






#-----------help functions to Saving product image in static/uploads/products Ordner--------------

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


def save_product_image(image_file):
    if not image_file or image_file.filename == "":
        return None

    if not allowed_file(image_file.filename):
        return None

    filename = secure_filename(image_file.filename)

    upload_folder = os.path.join(
        current_app.root_path,
        "static",
        "uploads",
        "products"
    )

    os.makedirs(upload_folder, exist_ok=True)

    image_path = os.path.join(upload_folder, filename)
    image_file.save(image_path)

    return f"uploads/products/{filename}"




#===================================Admin part=======================================

admin_product_bp = Blueprint("admin_product", __name__, url_prefix="/admin/products")


@admin_product_bp.route("/")
def admin_product_list():
    products = get_all_products()

    return render_template(
        "admin/products/products.html",
        products=products
    )
    
#--------------------------------------------------------

@admin_product_bp.route("/add_product", methods=["GET", "POST"])
def add_product_form():

    categories = get_all_categories()

    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        price = request.form.get("price")
        category = request.form.get("category")

        #image saving
        image_file = request.files.get("image_file")
        image_url = save_product_image(image_file)
        if not image_url:
            flash("Please upload a valid image file.", "danger")
            return redirect(url_for("admin_product.add_product_form"))

        create_product(name, description, price, category, image_url)

        flash("Product added successfully!", "success")

        return redirect(url_for("admin_product.add_product_form"))

    return render_template(
        "admin/products/add_product.html",
        categories=categories
    )

#-------------------------------------------------------------

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

#-----------------------------------------------------------------

@admin_product_bp.route("/<int:product_id>/delete")
def delete_product(product_id):

    product = get_product_by_id(product_id)

    if not product:
        flash("Product not found.", "danger")
        return redirect(url_for("admin_product.admin_product_list"))

    remove_product(product_id)

    flash("Product deleted successfully!", "success")
    return redirect(url_for("admin_product.admin_product_list"))

#--------------------------------------------------------------------


