import pytest
from log_collection import LogCollection

def test_valid_index():
    logs = LogCollection(['ERROR', 'WARNING', 'DEBUG'])
    assert logs[0] == 'ERROR'
    assert logs[-1] == 'DEBUG'

def test_out_of_bounds_index():
    logs = LogCollection(['ERROR', 'WARNING', 'DEBUG'])
    with pytest.raises(IndexError):
        _ = logs[10]

def test_invalid_index_type():
    logs = LogCollection(['ERROR', 'WARNING', 'DEBUG'])
    with pytest.raises(ValueError):
        _ = logs['invalid']