import pytest
from user import User
from admin import Admin
from artefact import Artefact
from database import Database
from encryption import generate_key

@pytest.fixture(scope="module")
def key():
    return generate_key()

@pytest.fixture
def db(key):
    return Database(encryption_key=key)

@pytest.fixture
def user():
    return User("test_user","test_password", "user")

@pytest.fixture
def admin():
    return Admin("test_admin","test_password")

@pytest.fixture
def artefact(key):
    return Artefact("test_artefact", "test_data", key)

def test_user_add_artefact(user, db, artefact):
    result = user.add_artefact(db, artefact)
    assert result is True

def test_user_remove_artefact(user, db, artefact):
    user.add_artefact(db, artefact)
    user.remove_artefact(db, "test_artefact")
    assert len(user.artefacts) == 0

def test_admin_create_artefact(admin, db, artefact):
    result = admin.create_artefact(db, artefact.name, artefact.data, artefact.key)
    assert result is True
    assert db.read_artefact(admin.username, "test_artefact") is not None

def test_admin_delete_artefact(admin, db, artefact):
    admin.create_artefact(db, artefact.name, artefact.data, artefact.key)
    result = admin.delete_artefact(db, "test_artefact")
    assert result is True
    assert db.read_artefact(admin.username, "test_artefact") is None
