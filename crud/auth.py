import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from . import db

# from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

# region
# @bp.route('/register', methods=('GET', 'POST'))
# def register():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         db = get_db()
#         error = None

#         if not username:
#             error = 'Username is required.'
#         elif not password:
#             error = 'Password is required.'

#         if error is None:
#             try:
#                 db.execute(
#                     "INSERT INTO user (username, password) VALUES (?, ?)",
#                     (username, generate_password_hash(password)),
#                 )
#                 db.commit()
#             except db.IntegrityError:
#                 error = f"User {username} is already registered."
#             else:
#                 return redirect(url_for("auth.login"))

#         flash(error)

#     return render_template('auth/register.html')
# endregion


@bp.route('/login', methods=('GET', 'POST'))
def login():
    # when submit
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        query = "select id, username, password, display_name from tblusers where username = %s limit 1 "
        params = (username,)
        error = None
        resp = db.executeQuery(query, params).get('data')
        if len(resp) <= 0:
            error = "Incorrect Username"
        elif not check_password_hash(resp[0][2], password):
            error = "Incorrect Password"

        if error is None:
            resp = resp[0]
            session.clear()
            session['user_id'] = resp[0]
            session['username'] = resp[1]
            session['display_name'] = resp[3]
            return redirect(url_for('index'))

        flash(error)

    # when user has been login
    if g.user is not None:
        print(g.user)
        flash('Selamat Datang !!')
        return redirect(url_for('index'))

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    username = session.get('username')
    display_name = session.get('display_name')

    if user_id is None:
        g.user = None
    else:
        g.user = user_id
        g.username = username
        g.display_name = display_name


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
