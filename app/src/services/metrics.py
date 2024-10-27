from prometheus_client import Counter, Gauge, Histogram

# Define metrics
REQUEST_COUNT = Counter(
    'request_count',
    'Total number of requests',
    ['method', 'endpoint'])

REQUEST_DURATION = Histogram(
    'request_duration_seconds',
    'Request duration in seconds',
    ['method', 'endpoint'])

REQUEST_IN_PROGRESS = Gauge(
    'request_in_progress',
    'Number of requests in progress',
    ['method', 'endpoint'])

ERROR_COUNT = Counter(
    'error_count',
    'Total number of errors',
    ['method', 'endpoint', 'status_code'])
