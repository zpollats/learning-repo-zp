from parser import LogEntry

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
	log_collector = LogCollection(['ERROR', 'WARNING', 'DEBUG'])
	print(log_collector)
	print(len(log_collector))
	print(log_collector[-1])
	print(log_collector[0:2])