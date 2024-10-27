from prometheus_client import Counter

# Define a custom metric with the namespace 'baywatch'
AUTH_REQUEST = Counter(
    'baywatch_auth_requests_total',
    'Total number of authentication requests',
    ['user', 'route'])
