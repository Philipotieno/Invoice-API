from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from instance.config import app_config

db = SQLAlchemy()


def create_app(env_name):
    
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[env_name])
    app.config.from_pyfile('config.py')
    db.init_app(app)
    
    @app.route('/')
    def hello_world():
        return 'Hello, World!'
    
    return app 
