import pytest
from admin import Admin
from database import Database
from artefact import Artefact
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
def admin(key):
    return Admin("test_admin", "test_password")

@pytest.fixture
def artefact(key):
    return Artefact("test_artefact", "test_data", key)

def test_create_admin(admin):
    assert admin.username == "test_admin"
    assert admin.role == "admin"

def test_create_artefact(admin, db, artefact):
    result = admin.create_artefact(db, artefact.name, artefact.data, artefact.key)
    assert result is True
    stored_artefact = db.read_artefact(admin.username, artefact.name)
    assert stored_artefact is not None
    assert stored_artefact.name == artefact.name
    assert stored_artefact.data == artefact.data
    assert stored_artefact.checksum == artefact.checksum

def test_delete_artefact(admin, db, artefact):
    result = admin.create_artefact(db, artefact.name, artefact.data, artefact.key)
    assert result is True
    stored_artefact = db.read_artefact('test_user', artefact.name)
    assert stored_artefact is None
