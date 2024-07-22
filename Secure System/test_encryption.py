import pytest
from encryption import generate_key, encrypt_data, decrypt_data

@pytest.fixture(scope="module")
def key():
    return generate_key()

def test_generate_key():
    key = generate_key()
    assert isinstance(key, str)
    assert len(key) > 0

def test_encrypt_decrypt_data(key):
    data = "test_data"
    encrypted_data = encrypt_data(data, key)
    decrypted_data = decrypt_data(encrypted_data, key)
    assert decrypted_data == data