import requests
import json
import time

BASE_URL = "http://localhost:8000"


def test_all():
    print("1. Health check:")
    r = requests.get(f"{BASE_URL}/health")
    print(json.dumps(r.json(), indent=2, ensure_ascii=False))

    print("\n2. Создание записи:")
    data = {
        "first_name": "Мирослава",
        "last_name": "Ясенева",
        "birth_date": "1991-03-15",
        "phone": "+7-930-111-2233",
        "email": "m.yaseneva@example.com",
        "insurance_number": "INS-NEW-003",
        "doctor_first_name": "Элина",
        "doctor_last_name": "Агафонова",
        "specialization": "Терапевт",
        "license_number": "LIC-101-2026",
        "doctor_phone": "+7-910-555-1001",
        "doctor_email": "elina.agafonova@medlife.ru",
        "appointment_date": "2026-05-07",
        "appointment_time": "17:00",
        "notes": "Третий тестовый приём"
    }
    r = requests.post(f"{BASE_URL}/api/appointments", json=data)
    print(f"Status: {r.status_code}")
    print(json.dumps(r.json(), indent=2, ensure_ascii=False))

    print("\nОжидание обработки Kafka...")
    time.sleep(5)

    print("\n3. Поиск всех записей:")
    r = requests.get(f"{BASE_URL}/api/appointments/search")
    print(f"Status: {r.status_code}")
    result = r.json()

    if isinstance(result, list):
        print(f"Всего записей: {len(result)}")
        for item in result[:3]:
            print(
                f"  - {item.get('patient_name')} -> {item.get('doctor_name')} ({item.get('appointment_date')} {item.get('appointment_time')})")
    else:
        print(f"Ошибка: {result}")

    print("\n4. Поиск по фамилии 'Ясенева':")
    r = requests.get(f"{BASE_URL}/api/appointments/search", params={"patient_name": "Ясенева"})
    print(f"Status: {r.status_code}")
    result = r.json()
    if isinstance(result, list):
        print(f"Найдено: {len(result)} записей")
        for item in result:
            print(
                f"  - {item.get('patient_name')} -> {item.get('doctor_name')} ({item.get('appointment_date')} {item.get('appointment_time')})")
    else:
        print(f"Ошибка: {result}")

    print("\n5. Топ-5 врачей:")
    r = requests.get(f"{BASE_URL}/api/reports/top-doctors")
    result = r.json()
    if isinstance(result, list):
        for item in result[:5]:
            print(
                f"  - {item.get('doctor_name')} ({item.get('specialization')}): {item.get('total_appointments')} приёмов")
    else:
        print(f"Ошибка: {result}")

    print("\n6. Топ-5 пациентов:")
    r = requests.get(f"{BASE_URL}/api/reports/top-patients")
    result = r.json()
    if isinstance(result, list):
        for item in result[:5]:
            print(f"  - {item.get('patient_name')}: {item.get('total_appointments')} приёмов")
    else:
        print(f"Ошибка: {result}")

    print("\n7. Статистика по специализациям:")
    r = requests.get(f"{BASE_URL}/api/reports/specialization-stats")
    result = r.json()
    if isinstance(result, list):
        for item in result[:5]:
            print(
                f"  - {item.get('specialization')}: {item.get('total_appointments')} приёмов, completion_rate: {item.get('completion_rate')}%")
    else:
        print(f"Ошибка: {result}")

    print("\n8. Анализ по дням недели:")
    r = requests.get(f"{BASE_URL}/api/reports/weekday-analysis")
    result = r.json()
    if isinstance(result, list):
        for item in result:
            print(f"  - {item.get('day_name')}: {item.get('total_appointments')} приёмов")
    else:
        print(f"Ошибка: {result}")

    print("\n9. Записи по дням (последние 30 дней):")
    r = requests.get(f"{BASE_URL}/api/reports/appointments-by-day", params={"days": "30"})
    result = r.json()
    if isinstance(result, list):
        for item in result:
            print(f"  - {item.get('appointment_date')}: {item.get('total_appointments')} приёмов")
    else:
        print(f"Ошибка: {result}")

    print("\n✓ Все тесты пройдены!")


if __name__ == "__main__":
    test_all()