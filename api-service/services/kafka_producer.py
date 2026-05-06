import json
import logging
from kafka import KafkaProducer
from config import KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC

logger = logging.getLogger(__name__)
_producer = None

def get_producer():
    global _producer
    if _producer is None:
        _producer = KafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            key_serializer=lambda k: k.encode('utf-8'),
            acks='all',
            retries=5,
            max_block_ms=10000
        )
        logger.info("Kafka producer initialized")
    return _producer

def send_appointment(key: str, data: dict):
    producer = get_producer()
    future = producer.send(
        KAFKA_TOPIC,
        key=key,
        value=data
    )
    metadata = future.get(timeout=30)
    logger.info(f"Sent key={key}, partition={metadata.partition}, offset={metadata.offset}")
    return metadata