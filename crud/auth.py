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
        resp = db.executeQuery(query, params)
        data_user = []

        if not resp:
            error = "Internal Server Error"
        else:
            data_user = resp.get('data')
            if len(data_user) <= 0:
                error = "Incorrect Username or Password"
            elif not check_password_hash(data_user[0]['password'], password):
                error = "Incorrect Username or Password"

        if error is None:
            query_get_group = """
            SELECT tg.id, tg.name as group_name, tg.status
            FROM rel_user_group rug
            LEFT JOIN tblgroups tg on tg.id=rug.id_group
            WHERE tg.status=TRUE and rug.id_user = %s
            order by tg.id
            """
            query_get_menu = """
            SELECT tm.id, tm.name as menu_name, tm.parent_id, tm.sequence, tm.parent_path, tm.img_menu, tm.action_link, tm.is_parent
            FROM rel_group_menu rgm 
            LEFT JOIN tblmenus tm on tm.id=rgm.id_menu
            WHERE tm.status=TRUE and rgm.id_group IN
            (
                SELECT id_group 
                FROM rel_user_group
                WHERE id_user= %s
            )
            ORDER BY tm.parent_id, tm.sequence
            """

            query_get_app_name = "SELECT par_name as app_name FROM tblsystem_parameter WHERE par_code='app_name' LIMIT 1"

            data_user = data_user[0]
            group = db.executeQuery(query_get_group, (data_user['id'],)).get('data')
            menu = db.executeQuery(query_get_menu, (data_user['id'],)).get('data')
            app_name = db.executeQuery(query_get_app_name).get('data')

            session.clear()
            # set user information
            session['id_user'] = data_user['id']
            session['username'] = data_user['username']
            session['display_name'] = data_user['display_name']
            # set menu information
            session['menus'] = menu
            # set group user
            session['groups'] = group
            # set app name
            session['app_name'] = app_name[0]['app_name']
            print(app_name)
            # print(group)
            # print(menu)

            return redirect(url_for('index'))

        flash(error)

    # when user has been login
    if g.user is not None:
        print(g.user)
        flash('Selamat Datang !!')
        return redirect(url_for('index'))

    return render_template('auth/login.html.jinja')


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
