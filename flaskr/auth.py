#blueprint is way to organize a group of related views and other code. Then blueprint is registered with the application in factory function
import functools

from flask import (
    Blueprint, flash,g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth') #creates blueprint named 'auth', 2nd arg is '__name__' to indicate it is defined in the current module

@bp.route('/register', methods=('GET', 'POST')) #connects /register url with register view function
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username: #validates that username and password are not empty
            error = 'Username is required!'
        elif not password:
            error = 'Password is required!'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?,?)",
                    (username, generate_password_hash(password)) #hashes password for security !!READ MORE ON HASHING
                )
                db.commit() #call commit to save changes to db
            except db.IntegrityError:
                error = f"Username {username} is already taken."
            else:
                return redirect(url_for("auth.login")) #once registered successfully then redirected to login view
        
        flash(error) #shows user if something is wrong, like username missing or password missing

    return render_template('auth/register.html') #renders template containing HTML

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST' :
        username = request.form ['username']
        password = request.form ['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone() # returns a row from query, if none found then returns None

        if user is None:
            error = 'Username is incorrect or is not registered.'
        elif not check_password_hash(user['password'], password): #hashes the password and compares with stored hash and compares them
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request #registers function that runs before view function, no matter the URL
def load_loggin_in_user():
    user_id = session.get('user_id') #gets user_id from current session

    if user_id is None: #???Guessing user_id is none before login, then uses user_id in session so they don't have to login everytime
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout(): #clears session then redirects to home pageS
    session.clear()
    return redirect(url_for('index')) 

def login_required(view): #DECORATOR - a function that takes another function as arg, and returns another function
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login')) #if no user then redirects to login before view
        return view(**kwargs) # otherwise continues with original view
    
    return wrapped_view

