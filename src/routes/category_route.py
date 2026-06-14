
from flask import render_template, Blueprint, request, redirect, url_for, flash

from src.services.category_service import (
    create_category,
    get_all_categories,
    get_category_by_name,
    get_category_by_id,
    edit_category,
    remove_category
)

admin_category_bp = Blueprint(
    "admin_category",
    __name__,
    url_prefix="/admin/categories"
)


@admin_category_bp.route('/')
def category_list():
    categories = get_all_categories()

    return render_template(
        'admin/categories/categories.html',
        categories=categories
    )


@admin_category_bp.route('/add_category', methods=["GET", "POST"])
def add_category_form():

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()

        if not name:
            flash("Category name is required.", "danger")
            return redirect(url_for("admin_category.add_category_form"))

        existing_category = get_category_by_name(name)

        if existing_category:
            flash("This category already exists.", "warning")
            return redirect(url_for("admin_category.add_category_form"))

        create_category(name, description)

        flash("Category added successfully.", "success")
        return redirect(url_for("admin_category.add_category_form"))

    return render_template('admin/categories/add_categorie_form.html')



@admin_category_bp.route("/<int:category_id>/edit", methods=["GET", "POST"])
def edit_category_form(category_id):

    category = get_category_by_id(category_id)

    if not category:
        flash("Category not found.", "danger")
        return redirect(url_for("admin_category.category_list"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()

        if not name:
            flash("Category name is required.", "danger")
            return redirect(url_for("admin_category.edit_category_form", category_id=category_id))

        existing_category = get_category_by_name(name)

        if existing_category and existing_category["id"] != category_id:
            flash("This category already exists.", "warning")
            return redirect(url_for("admin_category.edit_category_form", category_id=category_id))

        edit_category(category_id, name, description)

        flash("Category updated successfully.", "success")
        return redirect(url_for("admin_category.category_list"))

    return render_template(
        "admin/categories/edit_category.html",
        category=category
    )


@admin_category_bp.route("/<int:category_id>/delete")
def delete_category(category_id):

    category = get_category_by_id(category_id)

    if not category:
        flash("Category not found.", "danger")
        return redirect(url_for("admin_category.category_list"))

    remove_category(category_id)

    flash("Category deleted successfully.", "success")
    return redirect(url_for("admin_category.category_list"))