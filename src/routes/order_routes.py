from flask import Blueprint, render_template, redirect, url_for, session, flash, request
from src.services.user_service import get_all_users
from src.services.product_service import get_all_products
from src.services.order_service import (
    create_order_from_cart,
    create_order_from_admin,
    get_orders_by_user,
    get_all_orders,
    get_order_details,
    change_order_status,
    remove_order
)
from src.services.security_event_service import create_security_event


order_bp = Blueprint(
    "order",
    __name__,
    url_prefix="/orders"
)


@order_bp.route("/")
def my_orders():
    if "user_id" not in session:
        flash("Please login first.", "warning")
        return redirect(url_for("login.login_page"))

    orders = get_orders_by_user(session["user_id"])

    return render_template(
        "shop/my_orders.html",
        orders=orders
    )


@order_bp.route("/create", methods=["POST"])
def create_order():
    if "user_id" not in session:
        flash("Please login first.", "warning")
        return redirect(url_for("login.login_page"))

    order_id = create_order_from_cart(session["user_id"])

    if not order_id:
        flash("Your cart is empty.", "warning")
        return redirect(url_for("cart.cart_page"))

    flash("Order created successfully!", "success")

    return redirect(url_for("order.my_orders"))



#---Vulnerable route---------
@order_bp.route("/<int:order_id>")
def order_detail(order_id):

    # Only authenticated users can access the order detail page.
    if "user_id" not in session:
        flash("Please login first.", "warning")
        return redirect(url_for("login.login_page"))

    # The order_id is taken from the URL.
    # Example: /orders/1
    # A malicious user can change it manually to /orders/2.
    order, items = get_order_details(order_id)

    # If the order does not exist, stop the request.
    if not order:
        flash("Order not found.", "danger")
        return redirect(url_for("order.my_orders"))

    # We compare the owner of the order with the logged-in user.
    if order["user_id"] != session["user_id"]:
        # We log the suspicious access as a security event.
        create_security_event(
            event_type="IDOR_SUCCESS",
            severity="High",
            description=f"User {session['user_id']} accessed order {order_id} owned by user {order['user_id']}.",
            user_id=session["user_id"],
            endpoint=request.path,
            ip_address=request.remote_addr,
            user_agent=request.headers.get("User-Agent")
        )

    return render_template(
        "shop/order_detail.html",
        order=order,
        items=items
    )


# ======================== Admin part =============================

admin_order_bp = Blueprint(
    "admin_order",
    __name__,
    url_prefix="/admin/orders"
)


@admin_order_bp.route("/add_order", methods=["GET", "POST"])
def add_order_form():

    users = get_all_users()
    products = get_all_products()

    if request.method == "POST":
        user_id = request.form.get("user_id")
        status = request.form.get("status")
        product_ids = request.form.getlist("product_ids")
        quantities = request.form.getlist("quantities")

        order_id = create_order_from_admin(
            user_id=user_id,
            status=status,
            product_ids=product_ids,
            quantities=quantities
        )

        if not order_id:
            flash("Please add at least one product.", "warning")
            return redirect(url_for("admin_order.add_order_form"))

        flash("Order created successfully.", "success")
        return redirect(url_for("admin_order.admin_order_detail", order_id=order_id))

    return render_template(
        "admin/orders/add_order.html",
        users=users,
        products=products
    )


@admin_order_bp.route("/")
def order_list():
    orders = get_all_orders()

    return render_template(
        "admin/orders/orders.html",
        orders=orders
    )


@admin_order_bp.route("/<int:order_id>")
def admin_order_detail(order_id):
    order, items = get_order_details(order_id)

    return render_template(
        "admin/orders/order_detail.html",
        order=order,
        items=items
    )


@admin_order_bp.route("/<int:order_id>/status", methods=["POST"])
def update_status(order_id):
    status = request.form.get("status")

    change_order_status(order_id, status)

    flash("Order status updated successfully.", "success")

    return redirect(url_for("admin_order.admin_order_detail", order_id=order_id))


@admin_order_bp.route("/<int:order_id>/delete")
def delete_order(order_id):

    order, items = get_order_details(order_id)

    if not order:
        flash("Order not found.", "danger")
        return redirect(url_for("admin_order.order_list"))

    remove_order(order_id)

    flash("Order deleted successfully.", "success")
    return redirect(url_for("admin_order.order_list"))