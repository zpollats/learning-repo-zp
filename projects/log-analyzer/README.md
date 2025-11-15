# Log Analyzer

A Python CLI tool for parsing and analyzing log files with structured output.

## Features

- Parse logs with severity levels (INFO, WARNING, ERROR)
- Filter by severity, date range, or keyword
- Object-oriented design with LogEntry and LogParser classes
- Comprehensive error handling

## Usage
```python
from log_analyzer import LogParser

parser = LogParser()
logs = parser.parse_file('sample_data/sample_logs_simple.txt')
errors = [log for log in logs if log.severity == 'ERROR']
```

## Testing
```bash
pytest tests/
```

## Skills Demonstrated

- OOP design patterns
- File parsing with regex
- Error handling
- Unit testing with pytest
