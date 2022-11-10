from flask import Blueprint, flash, g, redirect, render_template, request, url_for, current_app
from werkzeug.exceptions import abort

from crud.auth import login_required
from . import db
bp = Blueprint('home', __name__)


@bp.route('/')
@login_required
def index():
    res = db.executeQuery('select * from res_userss')
    if res['status'] == False:
        flash('Database Error')
    return render_template('index.html')
