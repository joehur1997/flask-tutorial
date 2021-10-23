import sqlite3

import click
from flask import current_app, g #g is special object that is unique for each request - used to store data accessed by mulitple functions during request **READ MORE
from flask.cli import ScriptInfo, with_appcontext

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'], #current_app is special object that points to flask app handling request **CREATED in app factory func??
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    db= g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables"""
    init_db() #see previous function
    click.echo('Initialized the database.')

def init_app(app):#guessing this function has to be in the db script becase of close_db and init_db_command args
    app.teardown_appcontext(close_db) #calls function to close db when cleaning up after response
    app.cli.add_command(init_db_command) #adds new command to be called with flask command






