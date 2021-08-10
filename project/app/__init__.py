import os
import yaml
from pathlib import Path 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dynaconf import FlaskDynaconf
import logging
import logging.config

db = SQLAlchemy()


def create_app():
    """Initialize the Flask app instance
    """
    app = Flask(__name__)
    dynaconf = FlaskDynaconf(extensions_list=True)
    with app.app_context():

        os.environ["ROOT_PATH_FOR_DYNACONF"] = app.root_path
        dynaconf.init_app(app)
        db.init_app(app)
        _configure_logging(app, dynaconf)

        # import the routes
        from . import home
        from . import api

        # register the blueprints
        app.register_blueprint(home.home_bp)
        app.register_blueprint(api.api_bp)

        # create the database if necessary
        db.create_all()

        return app


def _configure_logging(app, dynaconf):
    # configure logging
    logging_config_path = Path(app.root_path).parent / "logging_config.yaml"
    with open(logging_config_path, "r") as fh:
        logging_config = yaml.safe_load(fh.read())
        env_logging_level = dynaconf.settings.get("logging_level", "INFO").upper()
        logging_level = logging.INFO if env_logging_level == "INFO" else logging.DEBUG
        logging_config["handlers"]["console"]["level"] = logging_level
        logging_config["loggers"][""]["level"] = logging_level
        logging.config.dictConfig(logging_config)
