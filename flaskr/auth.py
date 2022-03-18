import functools

from flask import Blueprint, render_template, request, flash, redirect, url_for, session, g
from werkzeug.security import generate_password_hash, check_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if not user_id:
        g.user = None
    else:
        g.user = get_db().execute('SELECT * FROM users where id = ?', (user_id,)).fetchone()


def login_required(view):
    @functools.wraps(view)
    def wrapper(*args, **kwargs):
        if not g.user:
            return redirect(url_for('auth.login'))
        return view(*args, **kwargs)

    return wrapper


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        db = get_db()
        error = None

        if not username:
            error = 'Username is required'
        if not password:
            error = 'Password is required'
        if not confirm_password:
            error = 'Password confirmation is required'
        if password != confirm_password:
            error = 'Password and password confirmation must match'

        if not error:
            try:
                db.execute(
                    'INSERT INTO users (username, password) VALUES (?, ?)',
                    (username, generate_password_hash(password))
                )

                db.commit()
            except db.IntegrityError:
                error = f'User {username} is already registered.'
            else:
                flash('Registered successfully, please log in', 'info')
                return redirect(url_for('auth.login'))

        if error:
            flash(error, 'danger')

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db()
        error = None

        user = db.execute('SELECT * FROM users where username = ?', (username,)).fetchone()

        if not user:
            error = 'User not found'
        elif not check_password_hash(user['password'], password):
            error = 'Invalid password'

        if error:
            flash(error, 'danger')
        else:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('posts.index'))

    return render_template('auth/login.html')


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
