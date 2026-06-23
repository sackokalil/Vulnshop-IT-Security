from flask import Blueprint, render_template, redirect, url_for, session, flash, request, current_app
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
from flask import send_file
import os

from io import BytesIO
from flask import send_file
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import cm


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

#---------------------------------------------------


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



#---Vulnerable route---------------------------------
@order_bp.route("/<int:order_id>")
def order_detail(order_id):

    # Only authenticated users can access the order detail page.
    if "user_id" not in session:
        flash("Please login first.", "warning")
        return redirect(url_for("login.login_page"))

    # The order_id is taken from the URL.
    # Example: /orders/1
    # A malicious user can change it manually to /orders/18.
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


#------------------------------------

@order_bp.route("/<int:order_id>/invoice")
def download_invoice(order_id):
    if "user_id" not in session:
        flash("Please login first.", "warning")
        return redirect(url_for("login.login_page"))

    requested_file = request.args.get("file")

    if requested_file:
        project_root = os.path.abspath(
            os.path.join(current_app.root_path, "..")
        )

        invoice_folder = os.path.join(
            project_root,
            "files",
            "invoices"
        )

        # VULNERABILITY: Path Traversal
        # Example:
        # /orders/1/invoice?file=../../secret.txt
        file_path = os.path.join(invoice_folder, requested_file)

        create_security_event(
            event_type="PATH_TRAVERSAL_ATTEMPT",
            severity="High",
            description=f"User {session['user_id']} requested file: {requested_file}",
            user_id=session["user_id"],
            endpoint=request.full_path,
            ip_address=request.remote_addr,
            user_agent=request.headers.get("User-Agent")
        )

        return send_file(file_path, as_attachment=True)

    order, items = get_order_details(order_id)

    if not order:
        flash("Order not found.", "danger")
        return redirect(url_for("order.my_orders"))

    if order["user_id"] != session["user_id"]:
        flash("Access denied.", "danger")
        return redirect(url_for("order.my_orders"))

    pdf_buffer = BytesIO()

    pdf = canvas.Canvas(pdf_buffer, pagesize=A4)
    width, height = A4

    y = height - 2 * cm

    pdf.setFont("Helvetica-Bold", 22)
    pdf.drawString(2 * cm, y, "VulnShop Invoice")

    y -= 1.2 * cm

    pdf.setFont("Helvetica", 11)
    pdf.drawString(2 * cm, y, f"Invoice Number: INV-{order['id']}")
    y -= 0.6 * cm
    pdf.drawString(2 * cm, y, f"Order ID: {order['id']}")
    y -= 0.6 * cm
    pdf.drawString(2 * cm, y, f"Order Date: {order['created_at']}")
    y -= 0.6 * cm
    pdf.drawString(2 * cm, y, f"Customer: {order['username']}")
    y -= 0.6 * cm
    pdf.drawString(2 * cm, y, f"Email: {order['email']}")
    y -= 1.2 * cm

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(2 * cm, y, "Product")
    pdf.drawString(9 * cm, y, "Price")
    pdf.drawString(12 * cm, y, "Qty")
    pdf.drawString(14 * cm, y, "Total")

    y -= 0.3 * cm
    pdf.setStrokeColor(colors.grey)
    pdf.line(2 * cm, y, 19 * cm, y)
    y -= 0.7 * cm

    pdf.setFont("Helvetica", 10)

    for item in items:
        if y < 3 * cm:
            pdf.showPage()
            y = height - 2 * cm
            pdf.setFont("Helvetica", 10)

        product_name = item["product_name"]
        if len(product_name) > 35:
            product_name = product_name[:35] + "..."

        pdf.drawString(2 * cm, y, product_name)
        pdf.drawString(9 * cm, y, f"{item['price']} EUR")
        pdf.drawString(12 * cm, y, str(item["quantity"]))
        pdf.drawString(14 * cm, y, f"{item['total_price']} EUR")

        y -= 0.7 * cm

    y -= 0.5 * cm
    pdf.line(2 * cm, y, 19 * cm, y)
    y -= 0.8 * cm

    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(12 * cm, y, "Total:")
    pdf.drawString(14 * cm, y, f"{order['total_price']} EUR")

    y -= 1.5 * cm

    pdf.setFont("Helvetica", 9)
    pdf.drawString(2 * cm, y, "Thank you for shopping with VulnShop.")

    pdf.save()

    pdf_buffer.seek(0)

    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=f"invoice_{order['id']}.pdf",
        mimetype="application/pdf"
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

#----------------------------------

@admin_order_bp.route("/")
def order_list():
    orders = get_all_orders()

    return render_template(
        "admin/orders/orders.html",
        orders=orders
    )

#---------------------------------------------

@admin_order_bp.route("/<int:order_id>")
def admin_order_detail(order_id):
    order, items = get_order_details(order_id)

    return render_template(
        "admin/orders/order_detail.html",
        order=order,
        items=items
    )

#----------------------------------------------

@admin_order_bp.route("/<int:order_id>/status", methods=["POST"])
def update_status(order_id):

    if "user_id" not in session:
        flash("Please login first.", "warning")
        return redirect(url_for("login.login_page"))

    if session.get("role") != "Admin":
        flash("Access denied.", "danger")
        return redirect(url_for("home.home_page"))

    status = request.form.get("status")

    change_order_status(order_id, status)

    flash("Order status updated successfully.", "success")

    return redirect(
        url_for(
            "admin_order.admin_order_detail",
            order_id=order_id
        )
    )


#---------------------------------------------------------

@admin_order_bp.route("/<int:order_id>/delete")
def delete_order(order_id):

    order, items = get_order_details(order_id)

    if not order:
        flash("Order not found.", "danger")
        return redirect(url_for("admin_order.order_list"))

    remove_order(order_id)

    flash("Order deleted successfully.", "success")
    return redirect(url_for("admin_order.order_list"))