import os
import logging
import sys

from flasgger import Swagger
from flask import Flask
from flask.blueprints import Blueprint
from flask_cors import CORS

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

import presentation_layer.views as views

ENV = os.environ.get('DEPLOY_ENV', 'Development')

def create_app(deploy_env: str = ENV) -> Flask:
    server = Flask(__name__)
    
    CORS(server)
    server.config.from_object('src.config.{}Config'.format(deploy_env))
    db = SQLAlchemy(server)

    server.db = db

    server.config["SWAGGER"] = {
        "swagger_version": "3.0.2",
        "title": "Application",
        "specs": [
            {
                "version": "0.0.1",
                "title": "Application",
                "endpoint": "spec",
                "route": "/application/spec",
                "rule_filter": lambda rule: True,  # all in
            }
        ],
        "static_url_path": "/apidocs",
    }

    server.config['SWAGGER']['openapi'] = '3.0.2'

    Swagger(server)

    _register_bluerints(server)
    _configure_logger(server)

    Migrate(server,db)

    return server

def _register_bluerints(server:Flask):
    for blueprint in vars(views).values():
        if isinstance(blueprint, Blueprint):
            server.register_blueprint(blueprint)


def _configure_logger(server:Flask):
    logger = logging.getLogger("Kanastra")
    logger.setLevel(server.config["LOGS_LEVEL"])
    logger.addHandler(logging.StreamHandler(sys.stdout))

