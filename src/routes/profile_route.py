from flask import Blueprint, render_template, session, redirect, url_for, flash, request, current_app
from src.services.profile_service import (
    get_profile_cart_stats,
    get_user_profile,
    update_profile_image
)
from src.services.security_event_service import create_security_event
from werkzeug.utils import secure_filename
import os


profile_bp = Blueprint(
    "profile",
    __name__,
    url_prefix="/profile"
)


#---------------------------------------------------------------

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


def save_profile_picture(image_file):
    if not image_file or image_file.filename == "":
        return None

    # VULNERABILITY: Unrestricted File Upload
    #
    # The uploaded file is saved without validating its extension,
    # MIME type, or real content.
    #
    # A normal user can upload files such as:
    # - .html
    # - .js
    # - .svg
    # - .bat
    # - .exe

    filename = secure_filename(image_file.filename)

    upload_folder = os.path.join(
        current_app.root_path,
        "static",
        "uploads",
        "profiles"
    )

    # We could return None in this condition. but the purpose is to demonstrate file upload 
    #vulnerability. the condition here is then only used to create a security event.
    if not allowed_file(image_file.filename):
            create_security_event(
            event_type="UNRESTRICTED_FILE_UPLOAD",
            severity="High",
            description=f"User uploaded profile file without validation: {filename}",
            user_id=session.get("user_id"),
            endpoint=request.path,
            ip_address=request.remote_addr,
            user_agent=request.headers.get("User-Agent")
        )


    os.makedirs(upload_folder, exist_ok=True)

    file_path = os.path.join(upload_folder, filename)
    image_file.save(file_path)

    

    return f"uploads/profiles/{filename}"

#------------------------------------------------------------

@profile_bp.route("/")
def profile_page():

    if "user_id" not in session:
        flash("Please login first.", "warning")
        return redirect(url_for("login.login_page"))

    cart_stats = get_profile_cart_stats(session["user_id"])
    user = get_user_profile(session["user_id"])

    return render_template(
        "shop/profile.html",
        cart_stats=cart_stats,
        user=user
    )

#-----------------------------------------------------------

@profile_bp.route("/upload-picture", methods=["POST"])
def upload_picture():

    if "user_id" not in session:
        flash("Please login first.", "warning")
        return redirect(url_for("login.login_page"))

    image_file = request.files.get("profile_image")
    image_url = save_profile_picture(image_file)

    if not image_url:
        flash("Please upload a file.", "danger")
        return redirect(url_for("profile.profile_page"))

    update_profile_image(
        user_id=session["user_id"],
        profile_image=image_url
    )

    flash("Profile picture updated successfully.", "success")
    return redirect(url_for("profile.profile_page"))