from flask import Blueprint, render_template, request, redirect, url_for, flash
from src.services.user_service import (
    get_all_users,
    create_user_by_admin,
    get_user_by_email,
    get_user_by_id,
    update_user,
    update_user_status,
    delete_user
)
from src.services.session_service import get_all_sessions





#=========================================ADMIN PART====================================


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




@admin_user_bp.route('/<int:user_id>')
def detail_user(user_id):
    user = get_user_by_id(user_id)

    if not user:
        flash("User not found.", "danger")
        return redirect(url_for('admin_user.user_list'))

    return render_template('admin/users/detail_user.html', user=user)


@admin_user_bp.route('/<int:user_id>/status', methods=['POST'])
def change_user_status(user_id):
    status = request.form.get('status')

    if status not in ['Active', 'Blocked']:
        flash("Invalid status.", "danger")
        return redirect(url_for('admin_user.detail_user', user_id=user_id))

    update_user_status(user_id, status)

    flash("User status updated successfully.", "success")
    return redirect(url_for('admin_user.detail_user', user_id=user_id))


@admin_user_bp.route('/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_user(user_id):
    user = get_user_by_id(user_id)

    if not user:
        flash("User not found.", "danger")
        return redirect(url_for('admin_user.user_list'))

    if request.method == 'POST':
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        email = request.form.get('email', '').strip()
        role = request.form.get('role', 'User')
        status = request.form.get('status', 'Active')

        if not first_name or not last_name or not email:
            flash("All required fields must be filled.", "danger")
            return redirect(url_for('admin_user.edit_user', user_id=user_id))

        existing_user = get_user_by_email(email)

        if existing_user and existing_user["id"] != user_id:
            flash("This email is already used by another user.", "warning")
            return redirect(url_for('admin_user.edit_user', user_id=user_id))

        update_user(
            user_id=user_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            role=role,
            status=status
        )

        flash("User updated successfully.", "success")
        return redirect(url_for('admin_user.user_list'))

    return render_template('admin/users/edit_user.html', user=user)


@admin_user_bp.route('/<int:user_id>/delete', methods=['POST'])
def remove_user(user_id):
    user = get_user_by_id(user_id)

    if not user:
        flash("User not found.", "danger")
        return redirect(url_for('admin_user.user_list'))

    delete_user(user_id)

    flash("User deleted successfully.", "success")
    return redirect(url_for('admin_user.user_list'))


#----------------------------Role et session routes------------------------------

@admin_user_bp.route('/roles')
def roles_page():
    return render_template('admin/users/roles.html')


@admin_user_bp.route('/sessions')
def sessions_page():
    sessions = get_all_sessions()
    return render_template('admin/users/sessions.html', sessions=sessions)