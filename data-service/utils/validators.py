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
            date_val = datetime.strptime(data[date_field], '%Y-%m-%d')
            if date_field == 'birth_date' and date_val > datetime.now():
                return False, "Дата рождения не может быть в будущем"
            if date_field == 'appointment_date' and date_val < datetime.now().replace(hour=0, minute=0, second=0,
                                                                                      microsecond=0):
                return False, "Дата приёма не может быть в прошлом"
        except ValueError:
            return False, f"Неверный формат даты в поле {date_field}. Ожидается YYYY-MM-DD"

    try:
        time_val = datetime.strptime(data['appointment_time'], '%H:%M')
        if time_val.hour < 8 or time_val.hour > 18:
            return False, "Время приёма должно быть с 8:00 до 18:00"
    except ValueError:
        return False, "Неверный формат времени. Ожидается HH:MM"

    phone = data['phone'].replace('+', '').replace('-', '').replace(' ', '')
    if not phone.isdigit() or len(phone) < 10:
        return False, "Некорректный номер телефона (должен содержать минимум 10 цифр)"

    if data.get('email') and '@' not in data['email']:
        return False, "Некорректный email адрес"

    return True, ""