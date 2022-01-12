from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from config import config

bootstrap = Bootstrap()
db = SQLAlchemy()


def create_app(config_name):
    """
    Factory method to create a flask app instance
    :param config_name: application configuration environment
    :return: Flask app instance
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    bootstrap.init_app(app)
    db.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app

