from datetime import datetime


def validate_appointment_data(data):
    required_fields = [
        'first_name', 'last_name', 'birth_date', 'phone', 'insurance_number',
        'doctor_first_name', 'doctor_last_name', 'specialization', 'license_number',
        'doctor_phone', 'doctor_email',
        'appointment_date', 'appointment_time'
    ]

    missing = [f for f in required_fields if f not in data]
    if missing:
        return False, f"Отсутствуют поля: {', '.join(missing)}"

    for date_field in ['birth_date', 'appointment_date']:
        try:
            datetime.strptime(data[date_field], '%Y-%m-%d')
        except ValueError:
            return False, f"Неверный формат даты в поле {date_field}. Ожидается YYYY-MM-DD"

    try:
        datetime.strptime(data['appointment_time'], '%H:%M')
    except ValueError:
        return False, "Неверный формат времени. Ожидается HH:MM"

    return True, ""