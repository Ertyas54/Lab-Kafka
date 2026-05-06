import os

KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS')
DATABASE_URL = os.getenv('DATABASE_URL')
KAFKA_TOPIC = 'medical-appointments'
KAFKA_GROUP_ID = os.getenv('KAFKA_GROUP_ID')