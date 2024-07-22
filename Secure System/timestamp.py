from datetime import datetime

def get_current_timestamp():
    """Returns the current timestamp in ISO 8601 format."""
    return datetime.utcnow().isoformat() + 'Z'