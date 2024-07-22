import hashlib

class ChecksumGenerator:
    @staticmethod
    def generate_checksum(content):
        # Generates a SHA-256 checksum for the given content
        return hashlib.sha256(content.encode()).hexdigest()