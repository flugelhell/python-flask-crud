from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from crud.auth import login_required

bp = Blueprint("settings_menu", __name__, url_prefix='/settings')


@bp.route('/')
def index():
    # set active parent menu id
    if request.args.get('menu_id'):
        session['active_parent_menu_id'] = int(request.args.get('menu_id'))

    return redirect(url_for('settings_menu.menu_items'))


@bp.route("/menu_items", methods=['GET'])
@login_required
def menu_items():
    navigation_menu = get_navigation_menu(session.get('menus'), session.get('active_parent_menu_id'))
    return render_template('/settings/menu_items.html.jinja', navigation_menu=navigation_menu, title="Menu Items")


@bp.route("/menu_form", methods=['GET'])
@login_required
def menu_form():
    return render_template('/settings/menu_form.html')


# Navigation menu yang akan diproses oleh template
def get_navigation_menu(list_menu=[], active_parent_menu_id=None):
    navigation_menu = []
    for menu_item in list_menu:  # filter(lambda menu: str(menu['parent_id']) == str(active_parent_menu_id), list_menu):
        if menu_item['parent_id'] == active_parent_menu_id:
            menu_item['child_menu'] = []

            for child_menu in list_menu:
                if child_menu['parent_id'] == menu_item['id']:
                    menu_item['child_menu'].append(child_menu)

            navigation_menu.append(menu_item)

    return navigation_menu
