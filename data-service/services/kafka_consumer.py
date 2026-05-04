import json
import logging
import time
from kafka import KafkaConsumer
from config import KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC
from services.db import execute_query

logger = logging.getLogger(__name__)


def process_message(msg):
    data = msg.value
    logger.info(f"Processing appointment for {data['first_name']} {data['last_name']}")

    try:
        patient = execute_query(
            "SELECT patient_id FROM patients WHERE insurance_number = %s",
            (data['insurance_number'],)
        )

        if patient:
            patient_id = patient[0]['patient_id']
        else:
            existing_phone = execute_query(
                "SELECT patient_id FROM patients WHERE phone = %s",
                (data['phone'],)
            )
            if existing_phone:
                logger.warning(f"Phone {data['phone']} already exists, using existing patient")
                patient_id = existing_phone[0]['patient_id']
            else:
                patient_id = execute_query(
                    """INSERT INTO patients (first_name, last_name, birth_date, phone, email, insurance_number)
                       VALUES (%s, %s, %s, %s, %s, %s) RETURNING patient_id""",
                    (data['first_name'], data['last_name'], data['birth_date'],
                     data['phone'], data.get('email', ''), data['insurance_number']),
                    fetch=True
                )[0]['patient_id']

        doctor = execute_query(
            "SELECT doctor_id FROM doctors WHERE license_number = %s",
            (data['license_number'],)
        )

        if doctor:
            doctor_id = doctor[0]['doctor_id']
        else:
            doctor_id = execute_query(
                """INSERT INTO doctors (first_name, last_name, specialization, license_number, phone, email, experience_years)
                   VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING doctor_id""",
                (data['doctor_first_name'], data['doctor_last_name'], data['specialization'],
                 data['license_number'], data['doctor_phone'], data['doctor_email'],
                 data.get('experience_years', 0)),
                fetch=True
            )[0]['doctor_id']

        existing = execute_query(
            """SELECT appointment_id FROM appointments 
               WHERE doctor_id = %s AND appointment_date = %s AND appointment_time = %s
               AND status != 'cancelled'""",
            (doctor_id, data['appointment_date'], data['appointment_time'])
        )
        if existing:
            logger.warning(
                f"Time slot {data['appointment_date']} {data['appointment_time']} already taken for doctor {doctor_id}")
            return

        execute_query(
            """INSERT INTO appointments (patient_id, doctor_id, appointment_date, appointment_time, status, notes)
               VALUES (%s, %s, %s, %s, 'scheduled', %s)""",
            (patient_id, doctor_id, data['appointment_date'], data['appointment_time'],
             data.get('notes', '')),
            fetch=False
        )
        logger.info(f"Appointment created for patient {patient_id} with doctor {doctor_id}")

    except Exception as e:
        logger.error(f"Error processing message: {e}")


def start_consumer():
    while True:
        try:
            consumer = KafkaConsumer(
                KAFKA_TOPIC,
                bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                auto_offset_reset='earliest',
                enable_auto_commit=True,
                group_id='data-service-group',
                value_deserializer=lambda x: json.loads(x.decode('utf-8')),
                consumer_timeout_ms=10000
            )
            logger.info("Kafka consumer connected")
            for msg in consumer:
                if msg is not None:
                    process_message(msg)
        except Exception as e:
            logger.error(f"Kafka consumer error, reconnecting in 10s: {e}")
            time.sleep(10)