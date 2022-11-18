import functools
import json

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

        query = "SELECT id, username, password, display_name FROM tblusers WHERE username = %s and status=true LIMIT 1 "
        params = (username,)
        error = None
        resp = db.executeQuery(query, params).get('data')

        if resp == None:
            error = "Internal Server Error"
        elif len(resp) <= 0:
            error = "Incorrect Username"
        elif not check_password_hash(resp[0][2], password):
            error = "Incorrect Password"

        if error is None:
            query = """ SELECT id_user, tm.id as menu_id, tm.name, tm.parent_id, tm.sequence, tm.status, tm.parent_path, tm.img_menu, tm.action_link
                        FROM rel_user_menu rum
                        LEFT JOIN tblmenus tm on tm.id=rum.id_menu
                        WHERE rum.id_user = %s
                        ORDER BY tm.parent_id, tm.sequence

                    """

            menu = db.executeQuery(query, (resp[0][0],)).get('data')
            if menu == None:
                flash("Internal Server Error")

            resp = resp[0]
            session.clear()
            # set user information
            session['id_user'] = resp[0]
            session['username'] = resp[1]
            session['display_name'] = resp[3]
            # set menu information
            session['menus'] = menu
            # print(menu)

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
    id_user = session.get('id_user')
    username = session.get('username')
    display_name = session.get('display_name')

    if id_user is None:
        g.user = None
    else:
        g.user = id_user
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
