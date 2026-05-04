import os

KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:29092')
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://med_user:med_pass@database:5432/medical_db')
KAFKA_TOPIC = 'medical-appointments'