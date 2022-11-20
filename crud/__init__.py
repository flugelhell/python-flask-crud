import os

from flask import Flask, render_template


def page_not_found(e):
    return render_template('error.html.jinja', error_code='404', error_message=e), 404


def internal_server_error(e):
    return render_template('error.html.jinja', error_code='500', error_message=e), 500


def create_app():
    # create and configure the app
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    # app.config['SECRET_KEY'] = 'Flugelhell'

    # ensure the instance folder exists
    # try:
    #     os.makedirs(app.instance_path)
    # except OSError:
    #     pass

    # Error Page Handler
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, page_not_found)

    from . import home
    from . import auth
    from . import settings_menu as menu

    app.register_blueprint(home.bp)
    app.add_url_rule('/', endpoint='index')
    app.register_blueprint(auth.bp)
    app.register_blueprint(menu.bp)

    # from . import db
    # db.init_app(app)

    # from . import auth
    # app.register_blueprint(auth.bp)

    # from . import blog
    # app.register_blueprint(blog.bp)
    # app.add_url_rule('/', endpoint='index')
    print(app.config)

    return app
