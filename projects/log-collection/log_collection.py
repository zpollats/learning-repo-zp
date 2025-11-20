class LogEntry:
    def __init__(self, log_entry: str):
        self._log_entry = log_entry
        self.parse_log()

    def __repr__(self):
        return f"LogEntry(TIMESTAMP={self.timestamp}, LEVEL={self.level}, MESSAGE={self.message})"
    
    def parse_log(self):
        parts = self._log_entry.split(' ')
        if len(parts) < 4:
            raise ValueError(f"Malformed log entry: {self._log_entry}")
        
        self.timestamp = parts[0] + ' ' + parts[1]
        self.level = parts[2]
        self.message = ' '.join(parts[3:])

class LogCollection:
	def __init__(self, logs: list[LogEntry]):
		self._logs = logs

	def __repr__(self):
		return f"LogCollection({self._logs})"

	def __len__(self):
		return len(self._logs)

	def __getitem__(self, location):
		if isinstance(location, slice):
			return [self._logs[i] for i in range(*location.indices(len(self._logs)))]

		if not isinstance(location, int):
			raise ValueError(f"Invalid Index. Index must be an integer, not {type(location).__name__}")

		if location < -len(self._logs) or location >= len(self._logs):
			raise IndexError(f"Index {location} is out of bounds for LogCollection of length {len(self._logs)}")

		return self._logs[location]

if __name__ == '__main__':
	log_collector = LogCollection([LogEntry('ERROR'), LogEntry('WARNING'), LogEntry('INFO'), LogEntry('DEBUG')])
	print(log_collector)
	print(len(log_collector))
	print(log_collector[-1])
	print(log_collector[0:2])