import logging
import os
import sys

from celery import Celery
from flasgger import Swagger
from flask import Flask
from flask.blueprints import Blueprint
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

import presentation_layer.views as views

ENV = os.environ.get("DEPLOY_ENV", "Development")


def create_app(deploy_env: str = ENV) -> Flask:
    server = Flask(__name__)

    CORS(server)
    server.config.from_object("src.config.{}Config".format(deploy_env))
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
    server.config["CELERY_CONFIG"] = {}
    server.config["SWAGGER"]["openapi"] = "3.0.2"

    Swagger(server)

    _register_bluerints(server)
    _configure_logger(server)

    celery = _configure_celery(server)
    celery.set_default()
    server.extensions["celery"] = celery

    server.celery = celery

    Migrate(server, db)

    return server


def _register_bluerints(server: Flask) -> None:
    for blueprint in vars(views).values():
        if isinstance(blueprint, Blueprint):
            server.register_blueprint(blueprint)


def _configure_celery(server: Flask) -> None:
    celery = Celery(server.import_name)
    celery.conf.update(server.config["CELERY_CONFIG"])

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with server.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


def _configure_logger(server: Flask) -> None:
    logger = logging.getLogger("Kanastra")
    logger.setLevel(server.config["LOGS_LEVEL"])
    logger.addHandler(logging.StreamHandler(sys.stdout))
