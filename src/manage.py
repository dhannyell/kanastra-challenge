from flask import Flask
from flask import current_app as app
from flask.cli import FlaskGroup
from flask_migrate import Migrate

import config

server = Flask(__name__)
server.config["SQLALCHEMY_DATABASE_URI"] = config.BaseConfig.SQLALCHEMY_DATABASE_URI
cli = FlaskGroup(server)


@cli.command("initialize_table")
def create_db():
    app.db.drop_all()
    app.db.create_all()
    app.db.session.commit()


@cli.command("migrate")
def migrate():
    migrate = Migrate(server, app.db)
    migrate.init_app(server, app.db)


if __name__ == "__main__":
    cli()
