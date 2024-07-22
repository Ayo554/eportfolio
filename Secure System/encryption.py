from cryptography.fernet import Fernet, InvalidToken

def generate_key():
    """Generates a new encryption key."""
    return Fernet.generate_key().decode()

def encrypt_data(data, key):
    """Encrypts data using the provided key."""
    fernet = Fernet(key.encode())
    encrypted_data = fernet.encrypt(data.encode())
    return encrypted_data.decode()

def decrypt_data(encrypted_data, key):
    """Decrypts data using the provided key."""
    fernet = Fernet(key.encode())
    try:
        decrypted_data = fernet.decrypt(encrypted_data.encode())
        return decrypted_data.decode()
    except InvalidToken:
        raise ValueError("Invalid key or corrupted data")