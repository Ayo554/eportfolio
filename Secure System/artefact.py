import hashlib
import json
from encryption import encrypt_data, decrypt_data
from timestamp import get_current_timestamp

class Artefact:
    def __init__(self, name, data, key, created_at=None, updated_at=None):
        # Initializes an Artefact with given data and generates a checksum
        self.name = name
        self.data = data
        self.key = key
        self.checksum = self.calculate_checksum(data)
        self.created_at = created_at or get_current_timestamp()
        self.updated_at = updated_at or self.created_at

    def calculate_checksum(self, data):
        # Calculates the SHA-256 checksum of the given data
        return hashlib.sha256(data.encode()).hexdigest()

    def update_data(self, new_data):
        # Updates the artefact's data and recalculates checksum and timestamp
        self.data = new_data
        self.checksum = self.calculate_checksum(new_data)
        self.updated_at = get_current_timestamp()

    def to_dict(self):
        # Converts the artefact to a dictionary with encrypted data
        return {
            "name": self.name,
            "data": encrypt_data(self.data, self.key),
            "checksum": self.checksum,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, artefact_dict, key):
        # Creates an Artefact instance from a dictionary with decrypted data
        decrypted_data = decrypt_data(artefact_dict["data"], key)
        return cls(
            artefact_dict["name"],
            decrypted_data,
            key,
            artefact_dict["created_at"],
            artefact_dict["updated_at"],
        )

    def verify_checksum(self, checksum):
        # Verifies if the provided checksum matches the artefact's checksum
        return self.calculate_checksum(self.data) == checksum