import os

import pytest
from io import StringIO

from src.server import create_app


@pytest.fixture()
def app():
    os.environ["DEPLOY_ENV"] = "Testing"
    app = create_app("Testing")
    app.config["TESTING"] = True
    client = app.test_client()
    with app.app_context():
        app.db.metadata.bind = app.db.engine
        yield client
        app.db.session.rollback()


@pytest.fixture()
def csv_string():
    return StringIO(
        """name;governmentId;email;debtAmount;debtDueDate;debtId
    Elijah Santos;9558;janet95@example.com;7811;2024-06-26;ea23f2ca-663a-4266-a742-9da4c9f4fcb3
    """
    )
