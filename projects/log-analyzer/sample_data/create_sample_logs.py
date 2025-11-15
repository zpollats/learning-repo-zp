import random
from datetime import datetime, timedelta

levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
messages = {
    'ERROR': [
        'Database connection failed', 
        'Failed to process payment',
        'Authentication timeout',
        'API rate limit exceeded'
    ],
    'WARNING': [
        'High memory usage detected',
        'Slow query detected',
        'Cache miss',
        'Storage at capacity'
    ],
    'INFO': [
        'User login successful',
        'Request completed',
        'Service started',
        'Payment retry scheduled'
    ],
    'DEBUG': [
        'Processing request',
        'Cache lookup successful',
        'Database query',
        'Payment processed',
        'API call'
    ],
    'CRITICAL': [
        'System shutdown',
        'System out of memory',
        'Service unavailable',
        'Application crashed'
    ]
}

start_time = datetime.now()
with open('sample_logs_larger.txt', 'w') as f:
    for i in range(500):
        timestamp = start_time + timedelta(seconds=i*2)
        level = random.choice(levels)
        message = random.choice(messages[level])
        f.write(f"{timestamp.strftime('%Y-%m-%d %H:%M:%S')} {level} {message}\n")

print("Created sample logs file: 'sample_logs_larger.txt'")