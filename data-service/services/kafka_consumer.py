import json
import logging
import time
from kafka import KafkaConsumer
from config import KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC, KAFKA_GROUP_ID
from services.appointment_repository import save_appointment

logger = logging.getLogger(__name__)

def start_consumer():
    while True:
        try:
            consumer = KafkaConsumer(
                KAFKA_TOPIC,
                bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                auto_offset_reset='earliest',
                enable_auto_commit=True,
                group_id=KAFKA_GROUP_ID,
                value_deserializer=lambda x: json.loads(x.decode('utf-8')),
                consumer_timeout_ms=10000
            )
            logger.info(f"Kafka consumer connected with group '{KAFKA_GROUP_ID}'")
            for msg in consumer:
                if msg is not None:
                    try:
                        save_appointment(msg.value)
                    except Exception as e:
                        logger.error(f"Could not process message, skipping: {e}")
        except Exception as e:
            logger.error(f"Kafka consumer error, reconnecting in 10s: {e}")
            time.sleep(10)