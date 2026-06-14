from flask import Blueprint, render_template, session, redirect, url_for, flash
from src.services.profile_service import get_profile_cart_stats


profile_bp = Blueprint(
    "profile",
    __name__,
    url_prefix="/profile"
)


@profile_bp.route("/")
def profile_page():

    if "user_id" not in session:
        flash("Please login first.", "warning")
        return redirect(url_for("login.login_page"))

    cart_stats = get_profile_cart_stats(session["user_id"])

    return render_template(
        "shop/profile.html",
        cart_stats=cart_stats
    )