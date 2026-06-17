
from flask import Blueprint, request, redirect, url_for, flash, session
from src.services.review_service import create_review
from src.services.security_event_service import create_security_event


review_bp = Blueprint(
    "review",
    __name__,
    url_prefix="/reviews"
)


def contains_xss_payload(value):
    """
    Simple XSS detection helper for the security lab.

    This function checks whether the submitted review comment contains
    common HTML/JavaScript patterns used in Stored XSS attacks.

    Important:
    This is not a complete real-world XSS filter.
    It is only used here to detect suspicious payloads and create
    a security event for the VulnShop dashboard.
    """

    if not value:
        return False

    value = value.lower()

    suspicious_patterns = [
        "<script",
        "</script",
        "javascript:",
        "onerror=",
        "onload=",
        "onclick=",
        "alert(",
        "<img",
        "<svg",
        "<iframe",
        "<body",
        "<input",
        "<marquee"
    ]

    for pattern in suspicious_patterns:
        if pattern in value:
            return True

    return False


@review_bp.route("/product/<int:product_id>/add", methods=["POST"])
def add_review(product_id):

    # Read form values submitted by the user.
    reviewer_name = request.form.get("reviewerName", "").strip()
    rating = request.form.get("rating")
    comment = request.form.get("comment", "").strip()

    # Basic validation.
    if not reviewer_name:
        flash("Name is required.", "danger")
        return redirect(url_for("product.detail_product", product_id=product_id))

    if not comment:
        flash("Comment is required.", "danger")
        return redirect(url_for("product.detail_product", product_id=product_id))

    # Get current logged-in user ID if available.
    # If the user is not logged in, user_id will be None.
    user_id = session.get("user_id")


    # Detect suspicious Stored XSS content.
    if contains_xss_payload(comment):
        create_security_event(
            event_type="STORED_XSS_ATTEMPT",
            severity="High",
            description=f"Stored XSS payload submitted in review for product {product_id}.",
            user_id=user_id,
            endpoint=request.path,
            ip_address=request.remote_addr,
            user_agent=request.headers.get("User-Agent")
        )

    create_review(
        product_id=product_id,
        user_id=user_id,
        reviewer_name=reviewer_name,
        rating=int(rating),
        comment=comment
    )

    return redirect(url_for("product.detail_product", product_id=product_id))

