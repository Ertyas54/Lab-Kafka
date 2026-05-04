import os

KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:29092')
DATA_SERVICE_URL = os.getenv('DATA_SERVICE_URL', 'http://data-service:8081')
KAFKA_TOPIC = 'medical-appointments'