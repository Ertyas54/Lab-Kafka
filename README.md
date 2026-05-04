# Выбранная тема: Система записи на приём к врачу

Лабараторная работа №3 по Kafka. Микросервисная архитектура с использованием Docker, 
Kafka, PostgreSQL.

# Архитектура

1. HTTP Client - отправляет запросы к API Service; находится вне Docker-сети; может быть curl, браузер или Python скрипт.
2. API Service - принимает HTTP запросы от клиента; добавление записи: получает данные и отправляет их в Kafka; поиск и отчёты: перенаправляет запрос к Data Service; валидирует входные данные (даты, время, телефон, email); порт 8000.
3. Kafka - получает сообщения от API Service; хранит их в топике medical-appointments; отдаёт сообщения Data Service для последующей обработки; порт 9092.
4. Data Service - читает сообщения из Kafka и сохраняет их в БД; выполняет поиск по БД с фильтрацией по пациенту, врачу, специализации, датам и статусу; формирует отчёты с помощью SQL агрегаций (COUNT, AVG, GROUP BY); порт 8081.
5. PostgreSQL - хранит три таблицы: patients, doctors, appointments; таблицы связаны внешними ключами (patient_id, doctor_id); содержит тестовые данные с датами вокруг мая 2026 года; порт 5432.
6. Zookeeper - координирует работу Kafka; отслеживает состояние брокера; порт 2181.

# Запуск
```
docker-compose up --build
```

# API Endpoints с примерами

## Health check
```
curl http://localhost:8000/health
```
```
{
  "dependencies": {
    "data_service": "healthy",
    "kafka": "connected"
  },
  "service": "api-service",
  "status": "running"
}
```

## Добавление записи на приём
```
curl -X POST http://localhost:8000/api/appointments \
  -H "Content-Type: application/json" \
  -d '{
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
    "notes": "Тестовый приём"
  }'
```
```
{
  "appointment_info": {
    "date": "2026-05-07",
    "doctor": "Элина Агафонова",
    "patient": "Мирослава Ясенева",
    "time": "17:00"
  },
  "kafka_offset": 5,
  "message": "Запись на приём успешно создана"
}
```

## Поиск записей
```
curl "http://localhost:8000/api/appointments/search?patient_name=Ясенева"
```
```
[
  {
    "appointment_date": "2026-05-07",
    "appointment_id": 26,
    "appointment_time": "17:00",
    "diagnosis": null,
    "doctor_name": "Элина Агафонова",
    "notes": "Тестовый приём",
    "patient_name": "Мирослава Ясенева",
    "patient_phone": "+7-930-111-2233",
    "prescription": null,
    "specialization": "Терапевт",
    "status": "scheduled"
  }
]
```


## Топ-10 врачей по количеству приёмов
```
curl http://localhost:8000/api/reports/top-doctors
```
```
[
  {
    "cancelled": 1,
    "completed": 1,
    "completion_rate": "16.67",
    "doctor_name": "Элина Агафонова",
    "no_shows": 0,
    "specialization": "Терапевт",
    "total_appointments": 6
  },
  {
    "cancelled": 0,
    "completed": 2,
    "completion_rate": "66.67",
    "doctor_name": "Алиса Журавлёва",
    "no_shows": 0,
    "specialization": "Офтальмолог",
    "total_appointments": 3
  }
]
```
## Топ-10 пациентов по частоте записей
```
curl http://localhost:8000/api/reports/top-patients
```
```
[
  {
    "completed": 0,
    "insurance_number": "INS-NEW-003",
    "last_appointment": "2026-05-07",
    "no_shows": 0,
    "patient_name": "Мирослава Ясенева",
    "phone": "+7-930-111-2233",
    "total_appointments": 3
  },
  {
    "completed": 1,
    "insurance_number": "INS-A107-2026",
    "last_appointment": "2026-04-28",
    "no_shows": 0,
    "patient_name": "Веселина Федосеева",
    "phone": "+7-920-666-2008",
    "total_appointments": 2
  }
]
```
## Статистика по специализациям
```
curl http://localhost:8000/api/reports/specialization-stats
```
```
[
  {
    "completion_rate": "16.67",
    "doctor_count": 1,
    "no_show_rate": "0.00",
    "specialization": "Терапевт",
    "total_appointments": 6
  },
  {
    "completion_rate": "66.67",
    "doctor_count": 1,
    "no_show_rate": "0.00",
    "specialization": "Невролог",
    "total_appointments": 3
  }
]
```
## Анализ загрузки по дням недели
```
curl http://localhost:8000/api/reports/weekday-analysis
```
```
[
  {
    "active_doctors": 4,
    "avg_per_doctor": "1.00",
    "day_name": "Воскресенье",
    "total_appointments": 3
  },
  {
    "active_doctors": 3,
    "avg_per_doctor": "1.00",
    "day_name": "Понедельник",
    "total_appointments": 3
  },
  {
    "active_doctors": 4,
    "avg_per_doctor": "1.25",
    "day_name": "Четверг",
    "total_appointments": 5
  }
]
```
## Количество записей по дням
```
curl "http://localhost:8000/api/reports/appointments-by-day?days=30"
```
```
[
  {
    "appointment_date": "2026-05-07",
    "cancelled": 0,
    "completed": 0,
    "no_shows": 0,
    "scheduled": 3,
    "total_appointments": 3
  },
  {
    "appointment_date": "2026-05-06",
    "cancelled": 0,
    "completed": 0,
    "no_shows": 0,
    "scheduled": 2,
    "total_appointments": 2
  }
]
```

# Тестирование
Написан отдельный файл для тестирования всего функционала, находится в папке tests.

Быстрый запуск:
```
python tests/manual_test.py
```