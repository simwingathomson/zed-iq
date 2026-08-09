from datetime import datetime, timezone

from flask import Blueprint, jsonify, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required

from app import db
from app.models import Answer, Choice, Question, Quiz, Result
from app.utils import role_required

bp = Blueprint("quiz", __name__, url_prefix="/quiz")


@bp.route("/<int:quiz_id>/start", methods=["POST", "GET"])
@login_required
@role_required("student")
def start(quiz_id):
    quiz = db.get_or_404(Quiz, quiz_id)
    existing = Result.query.filter_by(quiz_id=quiz.id, student_id=current_user.id).first()
    if existing and existing.completed_at:
        return redirect(url_for("quiz.results", result_id=existing.id))
    if not existing:
        existing = Result(quiz_id=quiz.id, student_id=current_user.id, total=len(quiz.questions))
        db.session.add(existing)
        db.session.commit()
    session[f"quiz_{quiz.id}_index"] = len(existing.answers)
    return render_template("quiz/take.html", quiz=quiz, result=existing)


@bp.route("/<int:quiz_id>/question")
@login_required
@role_required("student")
def question(quiz_id):
    quiz = db.get_or_404(Quiz, quiz_id)
    result = Result.query.filter_by(quiz_id=quiz.id, student_id=current_user.id).first_or_404()
    answered = {a.question_id for a in result.answers}
    questions = sorted(quiz.questions, key=lambda item: item.order)
    next_question = next((q for q in questions if q.id not in answered), None)
    if not next_question:
        finish_result(result)
        return jsonify({"done": True, "results_url": url_for("quiz.results", result_id=result.id)})
    return jsonify(
        {
            "done": False,
            "number": len(answered) + 1,
            "total": len(questions),
            "timer": quiz.timer_seconds,
            "id": next_question.id,
            "text": next_question.text,
            "image": next_question.image,
            "choices": [{"label": c.label, "text": c.text} for c in sorted(next_question.choices, key=lambda c: c.label)],
        }
    )


@bp.route("/<int:quiz_id>/answer", methods=["POST"])
@login_required
@role_required("student")
def answer(quiz_id):
    data = request.get_json() or {}
    result = Result.query.filter_by(quiz_id=quiz_id, student_id=current_user.id).first_or_404()
    question = db.get_or_404(Question, int(data.get("question_id")))
    if Answer.query.filter_by(result_id=result.id, question_id=question.id).first():
        return jsonify({"ok": True})
    selected = data.get("selected") or "No Answer"
    correct_choice = Choice.query.filter_by(question_id=question.id, correct=True).first()
    correct = correct_choice is not None and selected == correct_choice.label
    db.session.add(Answer(result_id=result.id, question_id=question.id, selected_label=selected, correct=correct))
    db.session.commit()
    return jsonify({
        "ok": True,
        "correct": correct,
        "selected": selected,
        "correct_label": correct_choice.label if correct_choice else "",
        "correct_text": correct_choice.text if correct_choice else "",
    })


def finish_result(result):
    if result.completed_at:
        return
    result.score = sum(1 for a in result.answers if a.correct)
    result.total = len(result.quiz.questions)
    result.percentage = round((result.score / result.total) * 100, 1) if result.total else 0
    result.passed = result.percentage >= result.quiz.pass_mark
    result.completed_at = datetime.now(timezone.utc)
    result.time_taken = int((result.completed_at - result.started_at).total_seconds())
    db.session.commit()


@bp.route("/results/<int:result_id>")
@login_required
def results(result_id):
    result = db.get_or_404(Result, result_id)
    if current_user.role == "student" and result.student_id != current_user.id:
        return ("Forbidden", 403)
    finish_result(result)
    return render_template("quiz/results.html", result=result)
