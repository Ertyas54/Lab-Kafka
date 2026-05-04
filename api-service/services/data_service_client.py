import requests
from api_service.config import DATA_SERVICE_URL

def forward_request(endpoint: str, params=None):
    """Отправляет запрос к Data Service и возвращает (status_code, json_body)"""
    url = f"{DATA_SERVICE_URL}{endpoint}"
    try:
        resp = requests.get(url, params=params, timeout=10)
        return resp.status_code, resp.json()
    except requests.exceptions.RequestException as e:
        return 500, {"error": str(e)}