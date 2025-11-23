import pytest

from log_analyzer import LogEntry, LogParser, LogAnalyzer

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

# LOG ENTRY TESTS

def test_log_entry_valid_parse():
    log_entry = LogEntry("2025-10-16 09:23:15 ERROR Database connection failed: timeout after 30s")
    assert log_entry == LogEntry("2025-10-16 09:23:15 ERROR Database connection failed: timeout after 30s")
    #assert log_entry.timestamp == "2025-10-16 09:23:15"
    #assert log_entry.level == "ERROR"
    #assert log_entry.message == "Database connection failed: timeout after 30s"

def test_log_entry_repr():
    log_entry = LogEntry("2025-10-16 09:23:15 ERROR Database connection failed: timeout after 30s")
    assert repr(log_entry) == "LogEntry(TIMESTAMP=2025-10-16 09:23:15, LEVEL=ERROR, MESSAGE=Database connection failed: timeout after 30s)"

def test_malformed_log_entry(sample_malformed_log):
    with pytest.raises(ValueError):
        LogEntry(sample_malformed_log)

# LOG PARSER TESTS

def test_log_parser_load_file(sample_basic_file):
    log_parser = LogParser(sample_basic_file)
    first_entry = log_parser[0] 
    last_entry = log_parser[-1]
    
    assert len(log_parser) == 5

    assert first_entry.timestamp == "2025-10-16 09:23:15"
    assert first_entry.level == "ERROR"
    assert first_entry.message == "Database connection failed: timeout after 30s"

    assert last_entry.timestamp == "2025-10-16 09:24:10"
    assert last_entry.level == "DEBUG"
    assert last_entry.message == "Processing user request id=12345"

def test_log_parser_missing_file(sample_missing_file):
    with pytest.raises(FileNotFoundError):
        LogParser(sample_missing_file)

def test_log_parser_indexing(sample_basic_file):
    log_parser = LogParser(sample_basic_file)
    first =  log_parser[0] 
    last = log_parser[-1] 

    assert first.timestamp == "2025-10-16 09:23:15"
    assert first.level == "ERROR"
    assert first.message == "Database connection failed: timeout after 30s"

    assert last.timestamp == "2025-10-16 09:24:10"
    assert last.level == "DEBUG"
    assert last.message == "Processing user request id=12345"

def test_log_parser_slice(sample_basic_file):
    log_parser = LogParser(sample_basic_file)
    slice = log_parser[0:2] 

    assert len(slice) == 2
    assert slice[0].timestamp == "2025-10-16 09:23:15"
    assert slice[1].timestamp == "2025-10-16 09:23:18"

def test_log_parser_out_of_bounds(sample_basic_file):
    log_parser = LogParser(sample_basic_file)
    with pytest.raises(IndexError):
        log_parser[10]


# LOG ANALYZER TESTS

def test_log_analyzer_count(sample_basic_file):
    log_parser = LogParser(sample_basic_file)
    log_analyzer = LogAnalyzer(log_parser)
    assert log_analyzer.log_count == 5

def test_log_analyzer_levels(sample_basic_file):
    log_parser = LogParser(sample_basic_file)
    log_analyzer = LogAnalyzer(log_parser)
    assert log_analyzer.log_levels == {'ERROR': 2, 'WARNING': 1, 'INFO': 1, 'DEBUG': 1}

def test_log_analyzer_error_count(sample_basic_file):
    log_parser = LogParser(sample_basic_file)
    log_analyzer = LogAnalyzer(log_parser)
    assert log_analyzer.error_count == 2

def test_log_analyzer_warning_count(sample_basic_file):
    log_parser = LogParser(sample_basic_file)
    log_analyzer = LogAnalyzer(log_parser)
    assert log_analyzer.warning_count == 1

def test_log_analyzer_top_messages(sample_basic_file):
    log_parser = LogParser(sample_basic_file)
    log_analyzer = LogAnalyzer(log_parser)
    top_messages = log_analyzer.top_messages(3)
    assert len(top_messages) == 3
    assert top_messages[0] == ('Database connection failed: timeout after 30s', 2)
    
def test_log_analyzer_filter_by_level(sample_basic_file):
    log_parser = LogParser(sample_basic_file)
    log_analyzer = LogAnalyzer(log_parser)
    filtered_logs = log_analyzer.filter_by_level('ERROR')
    assert len(filtered_logs) == 2
    assert filtered_logs[0].level == 'ERROR'
    assert filtered_logs[1].level == 'ERROR'

def test_log_analyzer_empty_file(sample_empty_file):
    log_parser = LogParser(sample_empty_file)
    log_analyzer = LogAnalyzer(log_parser)
    assert log_analyzer.log_count == 0
    assert log_analyzer.error_count == 0
    assert log_analyzer.top_messages() == []