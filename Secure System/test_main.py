import pytest
from user import User
from admin import Admin
from artefact import Artefact
from database import Database
from encryption import generate_key
import os

@pytest.fixture(scope="module")
def key():
    return generate_key()

@pytest.fixture
def db(key):
    TEST_DB_PATH = 'data/test_db.json'
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)
    return Database(encryption_key=key)

@pytest.fixture
def user():
    return User("test_user", "test_password", "user")

@pytest.fixture
def admin():
    return Admin("test_admin", "test_password")

@pytest.fixture
def artefact(key):
    return Artefact("test_artefact", "test_data", key)

def test_user_operations(user, db, artefact):
    # User adds an artefact to the database
    result = user.add_artefact(db, artefact)
    assert result is True
    assert len(user.list_artefacts(db)) == 1

    # User lists their artefacts
    artefact_names = user.list_artefacts(db)
    assert len(artefact_names) == 1
    assert artefact_names[0] == "test_artefact"

    # User removes the artefact from the database
    result = user.remove_artefact(db, "test_artefact")
    assert result is True
    assert len(user.list_artefacts(db)) == 0

def test_admin_operations(admin, db, artefact):
    # Admin creates an artefact in the database
    content = artefact.data
    key = artefact.key
    result = admin.create_artefact(db, artefact.name, content, key)
    assert result is True
    assert db.read_artefact('test_admin', artefact.name) is not None

    # Admin deletes the artefact from the database
    result = admin.delete_artefact(db, artefact.name)
    assert result is True
    assert db.read_artefact('test_admin', artefact.name) is None

def test_main_flow(user, admin, db, artefact):
    # Simulate user operations
    test_user_operations(user, db, artefact)

    # Simulate admin operations
    test_admin_operations(admin, db, artefact)