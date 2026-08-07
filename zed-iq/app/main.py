from flask import Blueprint, render_template
from flask_login import current_user

from app.models import Quiz, Result

bp = Blueprint("main", __name__)


@bp.route("/")
def home():
    quizzes = Quiz.query.filter_by(active=True).order_by(Quiz.created_at.desc()).limit(6).all()
    return render_template("home.html", quizzes=quizzes)


@bp.route("/about")
def about():
    return render_template("about.html")


@bp.route("/leaderboard")
def leaderboard():
    results = (
        Result.query.filter(Result.completed_at.isnot(None))
        .order_by(Result.percentage.desc(), Result.time_taken.asc(), Result.completed_at.desc())
        .limit(50)
        .all()
    )
    return render_template("leaderboard.html", results=results, current_user=current_user)
