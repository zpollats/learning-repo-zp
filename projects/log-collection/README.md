# Log Collection

A custom Python class demonstrating magic methods for intuitive log manipulation.

## Features

- Implements `__len__` for counting logs
- Implements `__getitem__` for indexing and slicing
- Pythonic interface for log management

## Usage
```python
from log_collection import LogCollection

logs = LogCollection()
logs.add(log_entry)
print(len(logs))  # Uses __len__
first_log = logs[0]  # Uses __getitem__
```

## Testing
```bash
pytest tests/
```

## Skills Demonstrated

- Python magic methods
- Pythonic API design
- Unit testing
