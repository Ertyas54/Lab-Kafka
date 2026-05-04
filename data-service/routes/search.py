from flask import Blueprint, request, jsonify
from services.db import execute_query
from datetime import date, datetime, time as dt_time
import logging

logger = logging.getLogger(__name__)
search_bp = Blueprint('search', __name__)

@search_bp.route('/search/appointments', methods=['GET'])
def search_appointments():
    patient_name = request.args.get('patient_name', '')
    doctor_name = request.args.get('doctor_name', '')
    specialization = request.args.get('specialization', '')
    status = request.args.get('status', '')
    date_from = request.args.get('date_from', '')
    date_to = request.args.get('date_to', '')

    query = """
        SELECT a.appointment_id, a.appointment_date, a.appointment_time,
               a.status, a.diagnosis, a.prescription, a.notes,
               p.first_name || ' ' || p.last_name as patient_name,
               p.phone as patient_phone,
               d.first_name || ' ' || d.last_name as doctor_name,
               d.specialization
        FROM appointments a
        JOIN patients p ON a.patient_id = p.patient_id
        JOIN doctors d ON a.doctor_id = d.doctor_id
        WHERE 1=1
    """
    params = []

    if patient_name:
        query += " AND (p.first_name ILIKE %s OR p.last_name ILIKE %s)"
        params.extend([f'%{patient_name}%', f'%{patient_name}%'])
    if doctor_name:
        query += " AND (d.first_name ILIKE %s OR d.last_name ILIKE %s)"
        params.extend([f'%{doctor_name}%', f'%{doctor_name}%'])
    if specialization:
        query += " AND d.specialization ILIKE %s"
        params.append(specialization)
    if status:
        query += " AND a.status = %s"
        params.append(status)
    if date_from:
        query += " AND a.appointment_date >= %s::date"
        params.append(date_from)
    if date_to:
        query += " AND a.appointment_date <= %s::date"
        params.append(date_to)

    query += " ORDER BY a.appointment_date DESC, a.appointment_time DESC LIMIT 100"

    try:
        rows = execute_query(query, params)
        for row in rows:
            if isinstance(row.get('appointment_date'), date):
                row['appointment_date'] = row['appointment_date'].isoformat()
            if isinstance(row.get('appointment_time'), (datetime, dt_time)):
                row['appointment_time'] = row['appointment_time'].strftime('%H:%M')
        return jsonify(rows), 200
    except Exception as e:
        logger.error(f"Search error: {e}")
        return jsonify({"error": str(e)}), 500