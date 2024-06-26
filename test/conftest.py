import os
import pytest
from src.server import create_app

@pytest.fixture()
def app():
    os.environ["DEPLOY_ENV"] = "Testing"
    app = create_app('Testing')
    app.config['TESTING'] = True
    client = app.test_client()
    with app.app_context():
        app.db.metadata.bind = app.db.engine
        app.db.create_all() 
        yield client
        app.db.session.rollback()