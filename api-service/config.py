import os

KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS')
DATA_SERVICE_URL = os.getenv('DATA_SERVICE_URL')
KAFKA_TOPIC = 'medical-appointments'