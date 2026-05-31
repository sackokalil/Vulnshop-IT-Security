from flask import Blueprint, render_template


login_bp = Blueprint('login', __name__)
@login_bp.route('/login')
def login_page():
    return render_template('admin/login.html')


register_bp = Blueprint('register', __name__)
@register_bp.route('/register')
def register_page():
    return render_template('admin/register.html')