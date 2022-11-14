from flask import Blueprint, flash, g, redirect, render_template, request, url_for, current_app
from werkzeug.exceptions import abort

from crud.auth import login_required
from . import db
bp = Blueprint('home', __name__)


@bp.route('/')
@login_required
def index():
    return render_template('index.html')
