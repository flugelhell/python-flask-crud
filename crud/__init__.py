import os

from flask import Flask, render_template
from crud.auth import login_required


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

    from . import home
    from . import hello
    from . import auth

    app.register_blueprint(home.bp)
    app.add_url_rule('/', endpoint='index')
    app.register_blueprint(hello.bp)
    app.register_blueprint(auth.bp)

    # from . import db
    # db.init_app(app)

    # from . import auth
    # app.register_blueprint(auth.bp)

    # from . import blog
    # app.register_blueprint(blog.bp)
    # app.add_url_rule('/', endpoint='index')
    print(app.config)

    return app
