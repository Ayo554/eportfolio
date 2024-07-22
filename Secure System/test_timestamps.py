import pytest
from timestamp import get_current_timestamp

def test_get_current_timestamp():
    timestamp = get_current_timestamp()
    assert isinstance(timestamp, str)
    assert len(timestamp) > 0
    assert 'T' in timestamp
    assert 'Z' in timestamp