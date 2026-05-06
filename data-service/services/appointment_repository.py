import logging
from services.db import execute_query

logger = logging.getLogger(__name__)

def save_appointment(data: dict):
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

        duplicate = execute_query(
            """SELECT appointment_id FROM appointments
               WHERE patient_id = %s AND doctor_id = %s
               AND appointment_date = %s AND appointment_time = %s
               AND status = 'scheduled'""",
            (patient_id, doctor_id, data['appointment_date'], data['appointment_time'])
        )
        if duplicate:
            logger.warning("Patient already has appointment at this time with this doctor")
            return

        existing = execute_query(
            """SELECT appointment_id FROM appointments
               WHERE doctor_id = %s AND appointment_date = %s AND appointment_time = %s
               AND status != 'cancelled'""",
            (doctor_id, data['appointment_date'], data['appointment_time'])
        )
        if existing:
            logger.warning(f"Time slot {data['appointment_date']} {data['appointment_time']} already taken for doctor {doctor_id}")
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
        logger.error(f"Failed to save appointment: {e}")
        raise e