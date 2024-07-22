import pytest
import os
from database import Database
from artefact import Artefact
from encryption import generate_key

TEST_DB_PATH = 'data/test_db.json'
TEST_KEY = generate_key()

@pytest.fixture(scope="module")
def db():
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)
    return Database(encryption_key=TEST_KEY)

@pytest.fixture
def artefact():
    # Create an artefact for testing
    return Artefact("test_artefact", "test_data", TEST_KEY)

def test_create_database(db):
    assert db is not None

def test_add_artefact(db, artefact):
    # Add artefact to the database
    result = db.add_artefact('test_user', artefact.to_dict())
    assert result is True

def test_read_artefact(db, artefact):
    db.add_artefact('test_user', artefact.to_dict())
    stored_artefact = db.read_artefact('test_user', artefact.name)
    assert stored_artefact is not None
    assert stored_artefact.name == artefact.name
    assert stored_artefact.data == artefact.data
    assert stored_artefact.checksum == artefact.checksum

def test_update_artefact(db, artefact):
    db.add_artefact('test_user', artefact.to_dict())
    new_data = "new_data"
    result = db.update_artefact('test_user', artefact.name, new_data)
    assert result is True
    updated_artefact = db.read_artefact('test_user', artefact.name)
    assert updated_artefact is not None
    assert updated_artefact.data == new_data
    assert updated_artefact.checksum == Artefact(artefact.name, new_data, artefact.key).checksum


def test_delete_artefact(db, artefact):
    # Add artefact, then delete it
    db.add_artefact('test_user', artefact.to_dict())
    result = db.delete_artefact('test_user', artefact.name)
    assert result is True
    data = db.read_artefact('test_user', artefact.name)
    assert data is None

# Cleanup
def test_cleanup():
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)
