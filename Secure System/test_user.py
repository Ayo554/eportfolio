import pytest
from user import User
from artefact import Artefact
from encryption import generate_key
from database import Database
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
    return User("test_user","test_password", "user")

@pytest.fixture
def artefact(key):
    return Artefact("test_artefact", "test_data", key)

def test_create_user():
    user = User("test_user","test_password", "user")
    assert user.username == "test_user"
    assert user.role == "user"
    assert user.artefacts == []

def test_add_artefact(user, db, artefact):
    result = user.add_artefact(db, artefact)
    assert result is True
    assert len(user.artefacts) == 1
    assert user.artefacts[0].name == "test_artefact"

def test_remove_artefact(user, db, artefact):
    user.add_artefact(db, artefact)
    user.remove_artefact(db, "test_artefact")
    assert len(user.artefacts) == 0
"""
def test_get_artefact(user, db, artefact):
    user.add_artefact(db, artefact)
    retrieved_artefact = user.get_artefact(db, "test_artefact")
    assert retrieved_artefact is not None
    assert retrieved_artefact.to_dict() == artefact.to_dict()
"""

def test_list_artefacts(user, db, artefact):
    user.add_artefact(db, artefact)
    artefact_names = user.list_artefacts(db)
    assert len(artefact_names) == 1
    assert artefact_names[0] == "test_artefact"
