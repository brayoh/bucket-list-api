from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy

# import config file
from config import app_config
from app.endpoints import bucketlist_blueprint

# initialize sql-alchemy
db = SQLAlchemy()

def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    app.register_blueprint(bucketlist_blueprint)
    return app
