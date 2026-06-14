from flask import Blueprint, render_template, request, redirect, url_for, flash
from src.services.user_service import get_all_users, create_user_by_admin, get_user_by_email





#-----------------------------ADMIN PART--------------------


admin_user_bp = Blueprint(
    'admin_user',
    __name__,
    url_prefix='/users'
)


@admin_user_bp.route('/')
def user_list():
    users = get_all_users()
    return render_template('admin/users/users.html', users=users)


@admin_user_bp.route('/add', methods=['GET', 'POST'])
def add_user():

    if request.method == 'POST':
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        repeat_password = request.form.get('repeat_password', '')
        role = request.form.get('role', 'User')
        status = request.form.get('status', 'Active')

        if not first_name or not last_name or not email or not password:
            flash("All required fields must be filled.", "danger")
            return redirect(url_for('admin_user.add_user'))

        if password != repeat_password:
            flash("Passwords do not match.", "danger")
            return redirect(url_for('admin_user.add_user'))

        existing_user = get_user_by_email(email)

        if existing_user:
            flash("This email is already used.", "warning")
            return redirect(url_for('admin_user.add_user'))

        create_user_by_admin(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            role=role,
            status=status
        )

        flash("User created successfully.", "success")
        return redirect(url_for('admin_user.add_user'))

    return render_template('admin/users/add_user.html')

