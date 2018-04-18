import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(script_info=None):

    app = Flask(__name__)

    # set config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    db.init_app(app)

    from project.api.users import users_blueprint
    app.register_blueprint(users_blueprint)

    # Shell context for flask CLI
    app.shell_context_processor({'app': app, 'db': db})
    return app
