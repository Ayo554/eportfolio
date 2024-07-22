import pytest
from artefact import Artefact
from encryption import generate_key
from timestamp import get_current_timestamp
from datetime import datetime 

@pytest.fixture(scope="module")
def key():
    return generate_key()

def test_create_artefact(key):
    artefact = Artefact("test_artefact", "test_data", key)
    assert artefact.name == "test_artefact"
    assert artefact.data == "test_data"
    assert artefact.checksum == artefact.calculate_checksum("test_data")
    assert artefact.created_at == artefact.updated_at
    assert artefact.created_at <= get_current_timestamp()

def test_update_artefact(key):
    artefact = Artefact("test_artefact", "test_data", key)
    old_checksum = artefact.checksum
    old_timestamp = artefact.updated_at
    artefact.update_data("new_data")
    assert artefact.data == "new_data"
    assert artefact.checksum == artefact.calculate_checksum("new_data")
    assert artefact.checksum != old_checksum
    assert artefact.updated_at > old_timestamp

def test_artefact_to_dict(key):
    artefact = Artefact("test_artefact", "test_data", key)
    artefact_dict = artefact.to_dict()
    assert artefact_dict["name"] == "test_artefact"
    assert "data" in artefact_dict
    assert artefact_dict["checksum"] == artefact.calculate_checksum("test_data")
    assert artefact_dict["created_at"] == artefact.created_at
    assert artefact_dict["updated_at"] == artefact.updated_at

def test_artefact_from_dict(key):
    artefact = Artefact("test_artefact", "test_data", key)
    artefact_dict = artefact.to_dict()
    new_artefact = Artefact.from_dict(artefact_dict, key)
    assert new_artefact.name == artefact.name
    assert new_artefact.data == artefact.data
    assert new_artefact.checksum == artefact.checksum

    # Convert string to datetime for comparison
    original_created_at = datetime.fromisoformat(artefact.created_at.rstrip('Z'))
    new_created_at = datetime.fromisoformat(new_artefact.created_at.rstrip('Z'))
    original_updated_at = datetime.fromisoformat(artefact.updated_at.rstrip('Z'))
    new_updated_at = datetime.fromisoformat(new_artefact.updated_at.rstrip('Z'))

    # Assert that the timestamps are close within a small tolerance
    assert abs((new_created_at - original_created_at).total_seconds()) < 0.001
    assert abs((new_updated_at - original_updated_at).total_seconds()) < 0.001

def test_artefact_integrity(key):
    artefact = Artefact("test_artefact", "test_data", key)
    artefact_dict = artefact.to_dict()
    new_artefact = Artefact.from_dict(artefact_dict, key)
    assert new_artefact.calculate_checksum(new_artefact.data) == artefact.calculate_checksum("test_data")

def test_checksum_verification(key):
    artefact = Artefact("test_artefact", "test_data", key)
    correct_checksum = artefact.calculate_checksum("test_data")
    assert artefact.verify_checksum(correct_checksum) is True
    incorrect_checksum = artefact.calculate_checksum("wrong_data")
    assert artefact.verify_checksum(incorrect_checksum) is False
