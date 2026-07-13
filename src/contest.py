import json
import os
from datetime import datetime

from flask import (
    Blueprint, flash, redirect, render_template, request, session, url_for, current_app
)

from .db import get_app_db, get_contest_db

bp = Blueprint('contest', __name__)


def load_questions():
    questions_path = os.path.join(os.path.dirname(__file__), 'questions.json')
    with open(questions_path, 'r') as f:
        return json.load(f)


def login_required(view):
    import functools
    @functools.wraps(view)
    def wrapped(**kwargs):
        if not session.get('team_id'):
            return redirect(url_for('auth.index'))
        return view(**kwargs)
    return wrapped


def run_query(sql):
    try:
        db = get_contest_db()
        wrapped = f"SELECT * FROM ({sql}) AS result"
        result = db.execute(wrapped).fetchall()
        return [list(row) for row in result], None
    except Exception as e:
        return None, str(e)


def check_answer(answer_query, submitted_sql):
    db = get_contest_db()

    try:
        expected = db.execute(answer_query).fetchall()
        expected = sorted([list(row) for row in expected])
    except Exception as e:
        return False, f"Error running answer query: {str(e)}"

    result, error = run_query(submitted_sql)
    if error:
        return False, error

    if sorted(result) == expected:
        return True, None
    return False, "Result does not match expected output."


@bp.get('/questions')
@login_required
def questions():
    questions = load_questions()
    team_id = session['team_id']

    db = get_app_db()
    solved = db.execute(
        'SELECT question_id FROM submission WHERE team_id = ?',
        (team_id,)
    ).fetchall()
    solved_ids = {row['question_id'] for row in solved}

    total_score = sum(
        q['score'] for q in questions if q['id'] in solved_ids
    )

    return render_template(
        'questions.html',
        questions=questions,
        solved_ids=solved_ids,
        total_score=total_score,
        team_name=session['team_name']
    )


@bp.post('/submit')
@login_required
def submit():
    question_id = int(request.form.get('question_id'))
    submitted_sql = request.form.get('sql', '').strip()
    team_id = session['team_id']

    questions = load_questions()
    question = next((q for q in questions if q['id'] == question_id), None)

    if not question:
        return {'error': 'Question not found.'}, 404

    db = get_app_db()
    already_solved = db.execute(
        'SELECT submission_id FROM submission WHERE team_id = ? AND question_id = ?',
        (team_id, question_id)
    ).fetchone()

    if already_solved:
        return {'correct': True, 'message': 'Already solved!', 'score': question['score']}

    is_correct, error = check_answer(question['answer_query'], submitted_sql)

    if is_correct:
        db.execute(
            'INSERT INTO submission (team_id, question_id, submitted_sql, submitted_at) VALUES (?, ?, ?, ?)',
            (team_id, question_id, submitted_sql, datetime.utcnow().isoformat())
        )
        db.commit()
        return {'correct': True, 'message': 'Correct!', 'score': question['score']}

    return {'correct': False, 'message': error or 'Wrong answer, try again.'}