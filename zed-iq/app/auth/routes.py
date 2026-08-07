from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app import db
from app.models import School, User

bp = Blueprint("auth", __name__)


def _dashboard_for(user):
    if user.role in {"super_admin", "admin", "teacher"}:
        return url_for("admin.dashboard")
    return url_for("student.dashboard")


@bp.route("/login", methods=["GET", "POST"])
def student_login():
    if current_user.is_authenticated:
        return redirect(_dashboard_for(current_user))
    if request.method == "POST":
        student_id = request.form.get("student_id", "").strip().lower()
        user = User.query.filter_by(email=student_id, role="student").first()
        if user and user.check_password(request.form.get("password", "")) and user.active:
            login_user(user)
            return redirect(request.args.get("next") or url_for("student.dashboard"))
        flash("Invalid student ID or password.", "danger")
    return render_template("auth/student_login.html")


@bp.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if current_user.is_authenticated and current_user.role in {"super_admin", "admin", "teacher"}:
        return redirect(url_for("admin.dashboard"))
    if request.method == "POST":
        username = request.form.get("username", "").strip().lower()
        user = User.query.filter(User.email == username, User.role.in_(["super_admin", "admin", "teacher"])).first()
        if user and user.check_password(request.form.get("password", "")) and user.active:
            login_user(user, remember=bool(request.form.get("remember")))
            return redirect(request.args.get("next") or url_for("admin.dashboard"))
        flash("Invalid administrator credentials.", "danger")
    return render_template("auth/admin_login.html")


@bp.route("/register", methods=["GET", "POST"])
def register():
    schools = School.query.order_by(School.name).all()
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        if User.query.filter_by(email=email).first():
            flash("That student ID is already registered.", "warning")
            return redirect(url_for("auth.register"))
        user = User(
            name=request.form.get("name", "").strip(),
            email=email,
            role="student",
            school_id=request.form.get("school_id") or None,
        )
        user.set_password(request.form.get("password", ""))
        db.session.add(user)
        db.session.commit()
        flash("Student account created. Please log in.", "success")
        return redirect(url_for("auth.student_login"))
    return render_template("auth/register.html", schools=schools)


@bp.route("/logout")
@login_required
def student_logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("main.home"))


@bp.route("/admin/logout")
@login_required
def admin_logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.admin_login"))


@bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    if current_user.role != "student":
        return redirect(url_for("admin.settings"))
    if request.method == "POST":
        current_user.name = request.form.get("name", current_user.name).strip()
        password = request.form.get("password", "")
        if password:
            current_user.set_password(password)
        db.session.commit()
        flash("Profile updated.", "success")
    return render_template("auth/profile.html")

