import functools
from datetime import datetime

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from .db import get_app_db

bp = Blueprint('auth', __name__)


@bp.route('/')
def index():
    if session.get('team_name'):
        return redirect(url_for('contest.questions'))
    return render_template('register.html')


@bp.post('/register')
def register():
    team_name = request.form.get('team_name', '').strip()

    if not team_name:
        flash('Team name cannot be empty.')
        return redirect(url_for('auth.index'))

    db = get_app_db()

    existing = db.execute(
        'SELECT team_id FROM team WHERE team_name = ?', (team_name,)
    ).fetchone()

    if existing:
        session['team_name'] = team_name
        session['team_id'] = existing['team_id']
        return redirect(url_for('contest.questions'))

    db.execute(
        'INSERT INTO team (team_name, joined_at) VALUES (?, ?)',
        (team_name, datetime.utcnow().isoformat())
    )
    db.commit()

    team = db.execute(
        'SELECT team_id FROM team WHERE team_name = ?', (team_name,)
    ).fetchone()

    session['team_name'] = team_name
    session['team_id'] = team['team_id']

    return redirect(url_for('contest.questions'))