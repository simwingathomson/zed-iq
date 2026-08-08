from flask import Blueprint, redirect, render_template, url_for
from flask_login import current_user, login_required

from app.models import Quiz, Result
from app.utils import role_required

bp = Blueprint("student", __name__)


@bp.route("/dashboard")
@login_required
@role_required("student")
def dashboard():
    completed_ids = [r.quiz_id for r in Result.query.filter_by(student_id=current_user.id).all()]
    upcoming = Quiz.query.filter(Quiz.active.is_(True), Quiz.id.not_in(completed_ids)).all()
    results = Result.query.filter_by(student_id=current_user.id).order_by(Result.completed_at.desc()).all()
    avg = round(sum(r.percentage for r in results) / len(results), 1) if results else 0
    ranked = (
        Result.query.filter(Result.completed_at.isnot(None))
        .order_by(Result.percentage.desc(), Result.time_taken.asc())
        .all()
    )
    position = next((i + 1 for i, r in enumerate(ranked) if r.student_id == current_user.id), None)
    return render_template("student/dashboard.html", upcoming=upcoming, results=results, avg=avg, position=position)


@bp.route("/quiz")
@login_required
@role_required("student")
def quiz_index():
    return redirect(url_for("student.dashboard"))


@bp.route("/results")
@login_required
@role_required("student")
def results_index():
    results = Result.query.filter_by(student_id=current_user.id).order_by(Result.completed_at.desc()).all()
    return render_template("student/results.html", results=results)
