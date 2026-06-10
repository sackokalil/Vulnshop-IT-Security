from flask import Blueprint, render_template

user_bp = Blueprint(
    'admin_user',
    __name__,
    url_prefix='/users'
)

@user_bp.route('/')
def user_list():
    return render_template('admin/users/users.html')