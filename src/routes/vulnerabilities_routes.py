from flask import Blueprint, render_template


admin_vulnerability_bp = Blueprint(
    "admin_vulnerability",
    __name__,
    url_prefix="/admin/vulnerabilities"
)


@admin_vulnerability_bp.route("/")
def vulnerability_dashboard():
    return render_template(
        "admin/security_lab/index.html"
    )


@admin_vulnerability_bp.route("/xss")
def xss_page():
    return render_template(
        "admin/security_lab/xss.html"
    )


@admin_vulnerability_bp.route("/sql-injection")
def sql_injection_page():
    return render_template(
        "admin/security_lab/sqli.html"
    )


@admin_vulnerability_bp.route("/idor")
def idor_page():
    return render_template(
        "admin/security_lab/idor.html"
    )

@admin_vulnerability_bp.route("/broken-authentication")
def broken_authentication_page():
    return render_template(
        "admin/security_lab/broken_auth.html"
    )


@admin_vulnerability_bp.route("/broken-access-control")
def broken_access_control_page():
    return render_template(
        "admin/security_lab/broken_access_control.html"
    )


@admin_vulnerability_bp.route("/path-traversal")
def path_traversal_page():
    return render_template(
        "admin/security_lab/path_traversal.html"
    )


@admin_vulnerability_bp.route("/csrf")
def csrf_page():
    return render_template(
        "admin/security_lab/csrf.html"
    )

@admin_vulnerability_bp.route("/file-upload")
def file_upload_page():
    return render_template(
        "admin/security_lab/file_upload.html"
    )


@admin_vulnerability_bp.route("/blind-sqli")
def blind_sqli_page():
    return render_template(
        "admin/security_lab/blind_sqli.html"
    )