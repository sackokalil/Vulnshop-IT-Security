from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from src.services.user_service import create_user, get_user_by_email
from src.services.auth_service import authenticate_user
from src.services.auth_service import authenticate_user, logout_user
import uuid
from src.services.session_service import create_session, end_session
from src.services.security_event_service import create_security_event



def contains_sql_injection_payload(value):
    """
    Simple SQL Injection detection helper for the security lab.

    This function checks whether a submitted login value contains
    common SQL Injection patterns.

    Important:
    This is not a complete real-world SQL Injection protection.
    It is only used here to detect suspicious payloads and create
    a security event for the VulnShop dashboard.
    """

    if not value:
        return False

    value = value.lower()

    suspicious_patterns = [
        "' or ",
        '" or ',
        " or 1=1",
        "'--",
        "--",
        "#",
        "/*",
        "*/",
        "union select",
        "drop table",
        "insert into",
        "delete from",
        "update users",
        "select ",
        "1=1"
    ]

    for pattern in suspicious_patterns:
        if pattern in value:
            return True

    return False



login_bp = Blueprint('login', __name__)
@login_bp.route('/login', methods=['GET', 'POST'])
def login_page():

    # User already logged in
    if "user_id" in session:

        if session.get("role") == "Admin":
            return redirect(url_for("admin.dashboard"))

        return redirect(url_for("profile.profile_page"))


    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        if not email:
            flash("Email is required.", "danger")
            return redirect(url_for("login.login_page"))

        if not password:
            flash("Password is required.", "danger")
            return redirect(url_for("login.login_page"))
        

        

        user = authenticate_user(email, password)

        if not user:
            flash("Invalid email or password.", "danger")
            return redirect(url_for("login.login_page"))

        if user["status"] != "Active":
            flash("Your account is not active.", "warning")
            return redirect(url_for("login.login_page"))

        session["user_id"] = user["id"]
        session["username"] = user["username"]
        session["email"] = user["email"]
        session["role"] = user["role"]

        session_token = str(uuid.uuid4())
        session["session_token"] = session_token

        create_session(
            user_id=user["id"],
            session_token=session_token,
            ip_address=request.remote_addr,
            user_agent=request.headers.get("User-Agent")
        )
        
        if contains_sql_injection_payload(email) or contains_sql_injection_payload(password):
            create_security_event(
                event_type="SQL_INJECTION_ATTEMPT",
                severity="High",
                description="SQL Injection payload submitted on login form.",
                user_id=None,
                endpoint=request.path,
                ip_address=request.remote_addr,
                user_agent=request.headers.get("User-Agent")
            )
            

        if user["role"] == "Admin":
            return redirect(url_for("admin.dashboard"))

        return redirect(url_for("profile.profile_page"))

    return render_template('auth/login.html')



register_bp = Blueprint("register", __name__, url_prefix="/register")
@register_bp.route("/", methods=["GET", "POST"])
def register_page():

    if request.method == "POST":
        first_name = request.form.get("first_name", "").strip()
        last_name = request.form.get("last_name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        repeat_password = request.form.get("repeat_password", "")

        if not first_name:
            flash("First name is required.", "danger")
            return redirect(url_for("register.register_page"))

        if not last_name:
            flash("Last name is required.", "danger")
            return redirect(url_for("register.register_page"))

        if not email:
            flash("Email is required.", "danger")
            return redirect(url_for("register.register_page"))

        if not password:
            flash("Password is required.", "danger")
            return redirect(url_for("register.register_page"))

        if password != repeat_password:
            flash("Passwords do not match!", "danger")
            return redirect(url_for("register.register_page"))
        
        existing_user = get_user_by_email(email)

        if existing_user:
            flash("This email is already used.", "warning")
            return redirect(url_for("register.register_page"))

        create_user(first_name, last_name, email, password)

        flash("Account created successfully! Please login.", "success")
        return redirect(url_for("login.login_page"))

    return render_template("auth/register.html")


logout_bp = Blueprint('logout', __name__)
@logout_bp.route("/logout")
def logout():
    session_token = session.get("session_token")

    if session_token:
        end_session(session_token)

    logout_user()

    flash("You have been logged out.", "success")
    return redirect(url_for("login.login_page"))