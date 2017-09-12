""" This file creates a flask instance of the app."""
import os
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# import config file
from config import app_config

# initialize sql alchemy
db = SQLAlchemy()

# import the api blueprint
from app.endpoints import bucketlist_blueprint


def create_app(config_name):
    """ Create app instance """
    app = FlaskAPI(__name__)
    app.config.from_object(app_config[config_name])
    CORS(app)
    db.init_app(app)
    app.register_blueprint(bucketlist_blueprint)

    return app
