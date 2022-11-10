from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from crud.auth import login_required

bp = Blueprint("setting_menus", __name__)


@bp.route("/menu_list", methods=['GET'])
@login_required
def menu_list():
    return render_template('settings/menu_list.html')


@bp.route("/menu_form", methods=['GET'])
@login_required
def menu_form():
    return render_template('settings/menu_form.html')
