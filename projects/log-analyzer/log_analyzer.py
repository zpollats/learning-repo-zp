from collections import defaultdict
import argparse

class LogEntry:
    def __init__(self, log_entry: str):
        self._log_entry = log_entry
        self.parse_log()

    def __repr__(self):
        return f"LogEntry(TIMESTAMP={self.timestamp}, LEVEL={self.level}, MESSAGE={self.message})"
    
    def __eq__(self, other):
        return self.timestamp == other.timestamp and self.level == other.level and self.message == other.message
    
    def parse_log(self):
        parts = self._log_entry.split(' ')
        if len(parts) < 4:
            raise ValueError(f"Malformed log entry: {self._log_entry}")
        
        self.timestamp = parts[0] + ' ' + parts[1]
        self.level = parts[2]
        self.message = ' '.join(parts[3:])

class LogParser:
    def __init__(self, log_file_path: str):
        self._log_file_path = log_file_path
        self._log_entries = []
        for line in self._file_reader_generator():
            self._log_entries.append(LogEntry(line.strip()))

    def __repr__(self):
        return f"LogParser({self._log_file_path})"
    
    def __len__(self):
        return len(self._log_entries)
    
    def __getitem__(self, location):
        if isinstance(location, slice):
            return [self._log_entries[i] for i in range(*location.indices(len(self._log_entries)))]

        if not isinstance(location, int):
            raise ValueError(f"Invalid Index. Index must be an integer, not {type(location).__name__}")

        if location < -len(self._log_entries) or location >= len(self._log_entries): 
            raise IndexError(f"Index {location} is out of bounds for LogCollection of length {len(self._log_entries)}")

        return self._log_entries[location]
    
    def _file_reader_generator(self):
        try:
            with open(self._log_file_path, 'r') as log_file:
                for line in log_file:
                    yield line
        except FileNotFoundError:
            raise FileNotFoundError(f"Log file provided does not exist: {self._log_file_path}")

class LogAnalyzer:
    def __init__(self, log_parser: LogParser):
        self._log_parser = log_parser

    def __repr__(self):
        return f"LogAnalyzer({self._log_parser})"
    
    @property
    def log_count(self):
        """Count of all log entries"""
        return len(self._log_parser)
    
    @property
    def error_count(self):
        """Count of all ERROR log entries"""
        return self.log_levels.get('ERROR', 0)

    @property
    def warning_count(self):
        """Count of all WARNING log entries"""
        return self.log_levels.get('WARNING', 0)
    
    @property
    def log_levels(self):
        log_level_dict = defaultdict(int)
        for log_entry in self._log_parser:
            log_level_dict[log_entry.level] += 1
        return log_level_dict
    
    @property
    def most_common_log_message(self):
        log_messages = defaultdict(int)
        for log_entry in self._log_parser:
            log_messages[log_entry.message] += 1
        max_message = max(log_messages, key=log_messages.get)
        return f"Most common log message: '{max_message}' with {log_messages[max_message]} occurrences."
    
    def top_messages(self, n: int = 5):
        """Returns the top n log messages"""
        log_messages = defaultdict(int)
        for log_entry in self._log_parser:
            log_messages[log_entry.message] += 1

        sorted_messages = sorted(log_messages.items(), key=lambda x: x[1], reverse=True)
        return sorted_messages[:n]
    
    def filter_by_level(self, level: str):
        """Returns all log entries with a speceified level"""
        return [entry for entry in self._log_parser if entry.level == level]

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Analyze log files.')
    parser.add_argument('filename', help='Path to log file')
    parser.add_argument('--level', help='Filter log entries by level', default=None)
    parser.add_argument('--top', type=int, help='Return top n log messages', default=5)

    args = parser.parse_args()

    log_parser = LogParser(args.filename)
    log_analyzer = LogAnalyzer(log_parser)

    print(f"Total logs: {log_analyzer.log_count}")
    print(f"Log levels: {dict(log_analyzer.log_levels)}")
    print(f"\nTop {args.top} log messages:")
    for msg, cnt in log_analyzer.top_messages(args.top):
        print(f"  {cnt:3d}x - {msg}")

    if args.level:
        filtered = log_analyzer.filter_by_level(args.level)
        print(f"\n{args.level} log entries: {len(filtered)}")