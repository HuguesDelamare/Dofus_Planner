import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from dofus_web_app.flaskr.db import get_db

# Create a Blueprint named 'auth' in the __name__ package
bp = Blueprint('auth', __name__, url_prefix='/auth')


# Call the register view and use the return value as the response
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        # If no Error, insert the new user data into the database
        if error is None:
            try:
                db.execute(
                    'INSERT INTO user (username, password) VALUES (?, ?)',
                    (username, generate_password_hash(password))
                )
                # Needs to be called afterwards to save the changes
                db.commit()
            # If the username is already registered, an error is raised
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for('auth.login'))
        flash(error)
    return render_template('auth/register.html')


# Call the login view and use the return value as the response
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Get the database connection
        db = get_db()
        error = None
        # Get the user data from the database
        # Returns one row from the query. If the query returned no results, it returns None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        # If the user does not exist or the password is wrong, raise an error
        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'
        # If no error, store the user id in a new session and return to index
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        flash(error)
    return render_template('auth/login.html')


# Register a function that runs before the view function, no matter what URL is requested
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    # If no user id is stored in the session, g.user will be None
    if user_id is None:
        g.user = None
    else:
        # If the user id is stored, get the user data from the database and store it in g.user
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


# Call the logout view and use the return value as the response
@bp.route('/logout')
def logout():
    # Remove the user id from the session
    session.clear()
    return redirect(url_for('index'))


# Create a decorator to check if a user is logged in
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
