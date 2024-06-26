import logging
import os

from dotenv import load_dotenv

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    DEPLOY_ENV = os.environ.get("DEPLOY_ENV", "Development")
    DEBUG = False
    APPLICATION_ROOT = os.getenv("APPLICATION_APPLICATION_ROOT", "/")
    HOST = os.getenv("APPLICATION_HOST")
    PORT = int(os.getenv("APPLICATION_PORT", "3000"))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_APP = os.environ.get("FLASK_APP")
    LOGS_LEVEL = logging.INFO

    DB_CONTAINER = os.environ.get("APPLICATION_DB_CONTAINER", "db")
    POSTGRES = {
        "user": os.getenv("APPLICATION_POSTGRES_USER", "postgres"),
        "pw": os.getenv("APPLICATION_POSTGRES_PW", ""),
        "host": os.getenv("APPLICATION_POSTGRES_HOST", DB_CONTAINER),
        "port": os.getenv("APPLICATION_POSTGRES_PORT", 5432),
        "db": os.getenv("APPLICATION_POSTGRES_DB", "postgres"),
    }
    SQLALCHEMY_DATABASE_URI = (
        "postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s" % POSTGRES
    )


class TestingConfig(BaseConfig):
    DEBUG = "TESTING"
    LOGS_LEVEL = logging.CRITICAL
    DEPLOY_ENV = "Testing"
    APPLICATION_ROOT = os.getenv("APPLICATION_APPLICATION_ROOT", "/")
    HOST = os.getenv("APPLICATION_HOST")
    PORT = int(os.getenv("APPLICATION_PORT", "3000"))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_APP = os.environ.get("FLASK_APP")

    DB_CONTAINER = os.environ.get("APPLICATION_DB_CONTAINER_TEST", "testdb")
    POSTGRES = {
        "user": os.getenv("APPLICATION_POSTGRES_USER", "test"),
        "pw": os.getenv("APPLICATION_POSTGRES_PW", "test"),
        "host": os.getenv("APPLICATION_POSTGRES_HOST", DB_CONTAINER),
        "port": os.getenv("APPLICATION_POSTGRES_PORT", 5433),
        "db": os.getenv("APPLICATION_POSTGRES_DB", "postgres"),
    }
    SQLALCHEMY_DATABASE_URI = (
        "postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s" % POSTGRES
    )


class StagingConfig(BaseConfig):
    pass


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    LOGS_LEVEL = int(os.environ.get("LOG_LEVEL", logging.INFO))


logging.basicConfig(
    filename=os.getenv("SERVICE_LOG", "server.log"),
    level=logging.DEBUG,
    format="%(levelname)s: %(asctime)s \
        pid:%(process)s module:%(module)s %(message)s",
    datefmt="%d/%m/%y %H:%M:%S",
)
