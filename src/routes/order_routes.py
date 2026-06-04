from flask import render_template, Blueprint

admin_order_bp = Blueprint(
    "admin_order",
    __name__,
    url_prefix="/admin/orders"
)


@admin_order_bp.route("/")
def order_list():
    return render_template("admin/orders/orders.html")


@admin_order_bp.route("/add_order")
def add_order_form():
    return render_template("admin/orders/add_order.html")