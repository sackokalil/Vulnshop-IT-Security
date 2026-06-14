from flask import Blueprint, render_template, session, redirect, url_for, flash
from src.services.dashboard_service import get_dashboard_stats


admin_dash_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_dash_bp.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        flash("Please login first.", "warning")
        return redirect(url_for("login.login_page"))

    if session.get("role") != "Admin":
        flash("Access denied. Only Admin can access the admin dashboard.", "danger")
        return redirect(url_for("home.home_page"))

    stats = get_dashboard_stats()

    return render_template(
        "admin/index.html",
        stats=stats
    )