# Word Counter

A text analysis tool for counting word frequencies in files. Built entirely without AI assistance to practice test-driven development.

## Features

- Count word frequencies in text files
- Case-insensitive counting
- Handles punctuation properly
- Comprehensive test suite with pytest fixtures

## Usage
```python
from word_counter import count_words

frequencies = count_words('sample.txt')
print(frequencies.most_common(10))
```

## Testing
```bash
pytest tests/ -v
```

## Skills Demonstrated

- Test-driven development
- pytest fixtures and tmp_path
- Edge case handling
- Clean, readable code
