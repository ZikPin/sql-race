import json
import os
import functools

from flask import (
    Blueprint, redirect, render_template, request, session, url_for, current_app
)

from .db import get_app_db

bp = Blueprint('admin', __name__, url_prefix='/admin')


def load_questions():
    questions_path = os.path.join(os.path.dirname(__file__), 'questions.json')
    with open(questions_path, 'r') as f:
        return json.load(f)


def admin_required(view):
    @functools.wraps(view)
    def wrapped(**kwargs):
        if not session.get('is_admin'):
            return redirect(url_for('admin.login'))
        return view(**kwargs)
    return wrapped


@bp.get('/login')
def login():
    return render_template('admin.html')


@bp.post('/login')
def login_post():
    password = request.form.get('password', '')
    admin_password = current_app.config.get('ADMIN_PASSWORD', 'admin')

    if password == admin_password:
        session['is_admin'] = True
        return redirect(url_for('admin.scores'))

    return render_template('admin.html', error='Wrong password.')


@bp.get('/scores')
@admin_required
def scores():
    return render_template('scores.html')


@bp.get('/scores/data')
@admin_required
def scores_data():
    questions = load_questions()
    db = get_app_db()

    teams = db.execute('SELECT team_id, team_name FROM team').fetchall()
    submissions = db.execute('SELECT team_id, question_id FROM submission').fetchall()

    solved_map = {}
    for row in submissions:
        solved_map.setdefault(row['team_id'], set()).add(row['question_id'])

    scoreboard = []
    for team in teams:
        team_id = team['team_id']
        solved = solved_map.get(team_id, set())
        total_score = sum(q['score'] for q in questions if q['id'] in solved)
        scoreboard.append({
            'team_name': team['team_name'],
            'total_score': total_score,
            'solved': list(solved)
        })

    scoreboard.sort(key=lambda x: x['total_score'], reverse=True)

    return {
        'questions': [{'id': q['id'], 'score': q['score']} for q in questions],
        'scoreboard': scoreboard
    }