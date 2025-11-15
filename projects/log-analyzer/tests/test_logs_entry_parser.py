import pytest

from parser import LogEntry, LogParser, LogAnalyzer

@pytest.fixture
def sample_missing_file(tmp_path):
    missing_file = tmp_path / 'missing_file.txt'
    return str(missing_file)

@pytest.fixture
def sample_empty_file(tmp_path):
    empty_file = tmp_path / 'empty_file.txt'
    empty_file.write_text("")
    return str(empty_file)

@pytest.fixture
def sample_basic_file(tmp_path):
    basic_file = tmp_path / 'basic_file.txt'
    basic_file.write_text(
        "2025-10-16 09:23:15 ERROR Database connection failed: timeout after 30s\n"
        "2025-10-16 09:23:18 WARNING Retrying connection attempt 1 of 3\n"
        "2025-10-16 09:23:21 ERROR Database connection failed: timeout after 30s\n"
        "2025-10-16 09:23:22 INFO Application started successfully\n"
        "2025-10-16 09:24:10 DEBUG Processing user request id=12345\n"
    )
    return str(basic_file)

@pytest.fixture
def sample_malformed_log(tmp_path):
    malformed_file = tmp_path / 'malformed_file.txt'
    malformed_file.write_text(
        "10/15/25 ERROR\n"
    )
    return str(malformed_file)

def test_missing_file(sample_missing_file):
    with pytest.raises(FileNotFoundError):
        LogParser(sample_missing_file)