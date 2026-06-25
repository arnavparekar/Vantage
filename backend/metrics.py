from prometheus_client import Counter, Histogram

webhook_events_total = Counter('webhook_events_total', 'Total webhook events received', ['repo', 'conclusion'])
webhook_processing_seconds = Histogram('webhook_processing_seconds', 'Time to process one webhook')
api_requests_total = Counter('api_requests_total', 'Total API requests', ['endpoint', 'status_code'])
api_request_duration_seconds = Histogram('api_request_duration_seconds', 'API request duration', ['endpoint'])
db_query_duration_seconds = Histogram('db_query_duration_seconds', 'DB query duration', ['query_name'])
