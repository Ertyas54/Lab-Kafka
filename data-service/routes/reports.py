from flask import Blueprint, request, jsonify
from services.db import execute_query
from datetime import date
import logging

logger = logging.getLogger(__name__)
reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/reports/top-doctors', methods=['GET'])
def top_doctors():
    query = """
        SELECT d.first_name || ' ' || d.last_name as doctor_name,
               d.specialization,
               COUNT(a.appointment_id) as total_appointments,
               COUNT(CASE WHEN a.status = 'completed' THEN 1 END) as completed,
               COUNT(CASE WHEN a.status = 'cancelled' THEN 1 END) as cancelled,
               COUNT(CASE WHEN a.status = 'no_show' THEN 1 END) as no_shows,
               ROUND(AVG(CASE WHEN a.status = 'completed' THEN 1 ELSE 0 END) * 100, 2) as completion_rate
        FROM doctors d
        LEFT JOIN appointments a ON d.doctor_id = a.doctor_id
        GROUP BY d.doctor_id, d.first_name, d.last_name, d.specialization
        ORDER BY total_appointments DESC
        LIMIT 10
    """
    return jsonify(execute_query(query)), 200

@reports_bp.route('/reports/appointments-by-day', methods=['GET'])
def appointments_by_day():
    days = request.args.get('days', '30')
    query = """
        SELECT appointment_date,
               COUNT(*) as total_appointments,
               COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed,
               COUNT(CASE WHEN status = 'scheduled' THEN 1 END) as scheduled,
               COUNT(CASE WHEN status = 'cancelled' THEN 1 END) as cancelled,
               COUNT(CASE WHEN status = 'no_show' THEN 1 END) as no_shows
        FROM appointments
        WHERE appointment_date >= CURRENT_DATE - INTERVAL %s
        GROUP BY appointment_date
        ORDER BY appointment_date DESC
    """
    rows = execute_query(query, (f'{days} days',))
    for row in rows:
        if isinstance(row.get('appointment_date'), date):
            row['appointment_date'] = row['appointment_date'].isoformat()
    return jsonify(rows), 200

@reports_bp.route('/reports/top-patients', methods=['GET'])
def top_patients():
    query = """
        SELECT p.first_name || ' ' || p.last_name as patient_name,
               p.phone, p.insurance_number,
               COUNT(a.appointment_id) as total_appointments,
               COUNT(CASE WHEN a.status = 'completed' THEN 1 END) as completed,
               COUNT(CASE WHEN a.status = 'no_show' THEN 1 END) as no_shows,
               MAX(a.appointment_date) as last_appointment
        FROM patients p
        JOIN appointments a ON p.patient_id = a.patient_id
        GROUP BY p.patient_id, p.first_name, p.last_name, p.phone, p.insurance_number
        ORDER BY total_appointments DESC
        LIMIT 10
    """
    rows = execute_query(query)
    for row in rows:
        if row.get('last_appointment') and isinstance(row['last_appointment'], date):
            row['last_appointment'] = row['last_appointment'].isoformat()
    return jsonify(rows), 200

@reports_bp.route('/reports/specialization-stats', methods=['GET'])
def specialization_stats():
    query = """
        SELECT d.specialization,
               COUNT(DISTINCT d.doctor_id) as doctor_count,
               COUNT(a.appointment_id) as total_appointments,
               ROUND(AVG(CASE WHEN a.status = 'completed' THEN 1.0 ELSE 0.0 END) * 100, 2) as completion_rate,
               ROUND(AVG(CASE WHEN a.status = 'no_show' THEN 1.0 ELSE 0.0 END) * 100, 2) as no_show_rate
        FROM doctors d
        LEFT JOIN appointments a ON d.doctor_id = a.doctor_id
        GROUP BY d.specialization
        ORDER BY total_appointments DESC
    """
    return jsonify(execute_query(query)), 200

@reports_bp.route('/reports/weekday-analysis', methods=['GET'])
def weekday_analysis():
    query = """
        SELECT EXTRACT(DOW FROM appointment_date) as day_of_week,
               CASE 
                   WHEN EXTRACT(DOW FROM appointment_date) = 0 THEN 'Воскресенье'
                   WHEN EXTRACT(DOW FROM appointment_date) = 1 THEN 'Понедельник'
                   WHEN EXTRACT(DOW FROM appointment_date) = 2 THEN 'Вторник'
                   WHEN EXTRACT(DOW FROM appointment_date) = 3 THEN 'Среда'
                   WHEN EXTRACT(DOW FROM appointment_date) = 4 THEN 'Четверг'
                   WHEN EXTRACT(DOW FROM appointment_date) = 5 THEN 'Пятница'
                   WHEN EXTRACT(DOW FROM appointment_date) = 6 THEN 'Суббота'
               END as day_name,
               COUNT(*) as total_appointments,
               COUNT(DISTINCT d.doctor_id) as active_doctors,
               ROUND(COUNT(*)::decimal / NULLIF(COUNT(DISTINCT d.doctor_id), 0), 2) as avg_per_doctor
        FROM appointments a
        JOIN doctors d ON a.doctor_id = d.doctor_id
        GROUP BY EXTRACT(DOW FROM appointment_date)
        ORDER BY day_of_week
    """
    return jsonify(execute_query(query)), 200