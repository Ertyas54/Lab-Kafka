from flask import Blueprint, request, jsonify
from config import DATA_SERVICE_URL
import requests
import logging

logger = logging.getLogger(__name__)
reports_bp = Blueprint('reports', __name__)

REPORTS = {
    'top-doctors': '/reports/top-doctors',
    'appointments-by-day': '/reports/appointments-by-day',
    'top-patients': '/reports/top-patients',
    'specialization-stats': '/reports/specialization-stats',
    'weekday-analysis': '/reports/weekday-analysis',
}


@reports_bp.route('/api/reports/<report_type>', methods=['GET'])
def get_report(report_type):
    if report_type not in REPORTS:
        return jsonify({"error": f"Unknown report: {report_type}"}), 404

    params = request.args.to_dict() if report_type == 'appointments-by-day' else None
    try:
        resp = requests.get(f"{DATA_SERVICE_URL}{REPORTS[report_type]}", params=params, timeout=10)
        return jsonify(resp.json()), resp.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500