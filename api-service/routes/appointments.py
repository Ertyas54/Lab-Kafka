from flask import Blueprint, request, jsonify
from services.kafka_producer import send_appointment
from utils.validators import validate_appointment_data
from config import DATA_SERVICE_URL
from datetime import datetime
import requests
import logging

logger = logging.getLogger(__name__)
appointments_bp = Blueprint('appointments', __name__)


@appointments_bp.route('/api/appointments', methods=['POST'])
def create_appointment():
    data = request.json
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400

    valid, msg = validate_appointment_data(data)
    if not valid:
        return jsonify({"error": msg}), 400

    payload = {
        "first_name": data['first_name'],
        "last_name": data['last_name'],
        "birth_date": data['birth_date'],
        "phone": data['phone'],
        "email": data.get('email', ''),
        "insurance_number": data['insurance_number'],
        "doctor_first_name": data['doctor_first_name'],
        "doctor_last_name": data['doctor_last_name'],
        "specialization": data['specialization'],
        "license_number": data['license_number'],
        "doctor_phone": data['doctor_phone'],
        "doctor_email": data['doctor_email'],
        "experience_years": data.get('experience_years', 0),
        "appointment_date": data['appointment_date'],
        "appointment_time": data['appointment_time'],
        "notes": data.get('notes', ''),
        "timestamp": datetime.now().isoformat()
    }

    try:
        metadata = send_appointment(payload)
        logger.info(
            f"Appointment created: {data['first_name']} {data['last_name']} -> {data['doctor_last_name']}, offset: {metadata.offset}")
        return jsonify({
            "message": "Запись на приём успешно создана",
            "appointment_info": {
                "patient": f"{data['first_name']} {data['last_name']}",
                "doctor": f"{data['doctor_first_name']} {data['doctor_last_name']}",
                "date": data['appointment_date'],
                "time": data['appointment_time']
            },
            "kafka_offset": metadata.offset
        }), 201
    except Exception as e:
        logger.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 500


@appointments_bp.route('/api/appointments/search', methods=['GET'])
def search():
    try:
        resp = requests.get(f"{DATA_SERVICE_URL}/search/appointments", params=request.args, timeout=10)
        return jsonify(resp.json()), resp.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500