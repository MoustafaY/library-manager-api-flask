import pytest
from app import create_app
from app.extensions import db as _db
from flask_jwt_extended import create_access_token

@pytest.fixture(scope="session")
def app():
    app = create_app(db_uri='sqlite:///test_db.sqlite')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
        _db.create_all()

    yield app

    with app.app_context():
        _db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

@pytest.fixture()
def teacher_token(app):
    with app.app_context():
        return create_access_token(identity="email@gmail.com")


@pytest.fixture()
def student_token(app):
    with app.app_context():
        return create_access_token(identity="joe@gmail.com")