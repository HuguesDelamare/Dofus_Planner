import os
from flask import Flask
from . import auth
from . import db


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # Set the path to the instance folder within the dofus_web_app folder
    instance_path = os.path.join(app.root_path, 'instance')

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists
    os.makedirs(instance_path, exist_ok=True)

    db.init_app(app)
    app.register_blueprint(auth.bp)

    # A simple page that says hello
    @app.route('/')
    def hello():
        return 'Hello, World!'

    return app
