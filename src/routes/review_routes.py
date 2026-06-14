from flask import Blueprint, request, redirect, url_for, flash, session
from src.services.review_service import create_review


review_bp = Blueprint(
    "review",
    __name__,
    url_prefix="/reviews"
)


@review_bp.route("/product/<int:product_id>/add", methods=["POST"])
def add_review(product_id):

    reviewer_name = request.form.get("reviewerName", "").strip()
    rating = request.form.get("rating")
    comment = request.form.get("comment", "").strip()

    if not reviewer_name:
        flash("Name is required.", "danger")
        return redirect(url_for("product.detail_product", product_id=product_id))

    if not comment:
        flash("Comment is required.", "danger")
        return redirect(url_for("product.detail_product", product_id=product_id))

    user_id = session.get("user_id")

    create_review(
        product_id=product_id,
        user_id=user_id,
        reviewer_name=reviewer_name,
        rating=int(rating),
        comment=comment
    )

    #flash("Review added successfully.", "success")

    return redirect(url_for("product.detail_product", product_id=product_id))