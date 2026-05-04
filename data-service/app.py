from flask import Flask, jsonify
from routes.search import search_bp
from routes.reports import reports_bp
from services.kafka_consumer import start_consumer
import threading
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    app.register_blueprint(search_bp)
    app.register_blueprint(reports_bp)

    @app.route('/health')
    def health():
        return jsonify({"status": "healthy", "service": "data-service"})

    return app

app = create_app()

if __name__ == '__main__':
    consumer_thread = threading.Thread(target=start_consumer, daemon=True)
    consumer_thread.start()
    logger.info("Kafka consumer thread started")
    app.run(host='0.0.0.0', port=8081, debug=False)