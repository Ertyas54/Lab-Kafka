from flask import Flask, jsonify
from services.kafka_producer import get_producer
from routes.appointments import appointments_bp
from routes.reports import reports_bp
from config import DATA_SERVICE_URL
import requests
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    app.register_blueprint(appointments_bp)
    app.register_blueprint(reports_bp)

    @app.route('/health')
    def health():
        kafka_status = "connected"
        try:
            producer = get_producer()
            producer.bootstrap_connected()
        except Exception as e:
            kafka_status = f"disconnected: {str(e)}"
            logger.error(f"Kafka health check failed: {e}")

        data_service_status = "unknown"
        try:
            resp = requests.get(f"{DATA_SERVICE_URL}/health", timeout=5)
            if resp.status_code == 200:
                data_service_status = "healthy"
            else:
                data_service_status = f"unhealthy (status {resp.status_code})"
        except Exception as e:
            data_service_status = f"unreachable: {str(e)}"

        return jsonify({
            "status": "running" if kafka_status == "connected" and data_service_status == "healthy" else "degraded",
            "service": "api-service",
            "dependencies": {
                "kafka": kafka_status,
                "data_service": data_service_status
            }
        })

    try:
        get_producer()
        logger.info("Kafka producer initialized")
    except Exception as e:
        logger.error(f"Failed to initialize Kafka producer: {e}")

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)