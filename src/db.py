import sqlite3
from datetime import datetime

import click
from flask import current_app, g


# Getting the databases
def get_contest_db():
    if 'contest_db' not in g:
        g.contest_db = sqlite3.connect(current_app.config['CONTEST_DATABASE'])
        g.contest_db.row_factory = sqlite3.Row
    return g.contest_db

def get_app_db():
    if 'app_db' not in g:
        g.app_db = sqlite3.connect(current_app.config['APP_DATABASE'])
        g.app_db.row_factory = sqlite3.Row
    return g.app_db


def close_db(exception):
    contest_db = g.pop('contest_db', None)
    app_db = g.pop('app_db', None)
    
    if contest_db is not None:
        contest_db.close()
    if app_db is not None:
        app_db.close()


# Initiliase the app database
def init_app_db():
    db = get_app_db()

    with current_app.open_resource('app_schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db:app')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_app_db()
    click.echo('Initialized the app database.')


# Initiliase the contest database
def init_contest_db():
    db = get_contest_db()

    with current_app.open_resource('contest_schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db:contest')
def init_contest_db_command():
    """Clear the existing data and create new tables for the contest."""
    init_contest_db()
    click.echo('Initialized the contest database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(init_contest_db_command)


sqlite3.register_converter(
    "timestamp", lambda v: datetime.fromisoformat(v.decode())
)