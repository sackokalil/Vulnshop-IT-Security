from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from src.services.cart_service import (
    add_product_to_cart,
    get_cart_by_user,
    remove_product_from_cart
)


cart_bp = Blueprint(
    "cart",
    __name__,
    url_prefix="/cart"
)


@cart_bp.route("/")
def cart_page():
    user_id = session.get("user_id")

    if not user_id:
        flash("Please login before accessing your cart.", "warning")
        return redirect(url_for("login.login_page"))

    cart_items = get_cart_by_user(user_id)

    total_price = 0

    for item in cart_items:
        total_price += item["total_price"]

    return render_template(
        "shop/cart.html",
        cart_items=cart_items,
        total_price=total_price
    )


@cart_bp.route("/add/<int:product_id>", methods=["POST"])
def add_cart_item(product_id):
    user_id = session.get("user_id")

    if not user_id:
        flash("Please login before adding products to cart.", "warning")
        return redirect(url_for("login.login_page"))

    quantity = request.form.get("quantity", 1)
    quantity = int(quantity)

    add_product_to_cart(
        user_id,
        product_id,
        quantity
    )

    flash("Product added to cart successfully!", "success")

    return redirect(url_for("cart.cart_page"))


@cart_bp.route("/remove/<int:cart_item_id>", methods=["POST"])
def remove_cart_item(cart_item_id):
    user_id = session.get("user_id")

    if not user_id:
        flash("Please login first.", "warning")
        return redirect(url_for("login.login_page"))

    remove_product_from_cart(
        cart_item_id,
        user_id
    )

    flash("Product removed from cart.", "success")

    return redirect(url_for("cart.cart_page"))