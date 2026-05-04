CREATE TABLE IF NOT EXISTS patients (
    patient_id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    birth_date DATE NOT NULL,
    phone VARCHAR(20) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE,
    insurance_number VARCHAR(50) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS doctors (
    doctor_id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    specialization VARCHAR(100) NOT NULL,
    license_number VARCHAR(50) UNIQUE NOT NULL,
    phone VARCHAR(20) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    experience_years INTEGER CHECK (experience_years >= 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS appointments (
    appointment_id SERIAL PRIMARY KEY,
    patient_id INTEGER NOT NULL,
    doctor_id INTEGER NOT NULL,
    appointment_date DATE NOT NULL,
    appointment_time TIME NOT NULL,
    status VARCHAR(20) DEFAULT 'scheduled'
        CHECK (status IN ('scheduled', 'completed', 'cancelled', 'no_show')),
    diagnosis TEXT,
    prescription TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE,
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id) ON DELETE CASCADE,
    UNIQUE(doctor_id, appointment_date, appointment_time)
);

CREATE INDEX idx_appointments_patient ON appointments(patient_id);
CREATE INDEX idx_appointments_doctor ON appointments(doctor_id);
CREATE INDEX idx_appointments_date ON appointments(appointment_date);
CREATE INDEX idx_appointments_status ON appointments(status);
CREATE INDEX idx_doctors_specialization ON doctors(specialization);
CREATE INDEX idx_patients_name ON patients(last_name, first_name);

-- Врачи (специализации: терапевт, кардиолог, невролог, ортопед, офтальмолог, эндокринолог, гастроэнтеролог, дерматолог)
INSERT INTO doctors (first_name, last_name, specialization, license_number, phone, email, experience_years) VALUES
('Элина', 'Агафонова', 'Терапевт', 'LIC-101-2026', '+7-910-555-1001', 'elina.agafonova@medlife.ru', 14),
('Руслан', 'Беспалов', 'Кардиолог', 'LIC-102-2026', '+7-910-555-1002', 'ruslan.bespalov@medlife.ru', 21),
('Варвара', 'Громова', 'Невролог', 'LIC-103-2026', '+7-910-555-1003', 'varvara.gromova@medlife.ru', 9),
('Арсений', 'Добровольский', 'Ортопед', 'LIC-104-2026', '+7-910-555-1004', 'arseniy.dobrovolsky@medlife.ru', 16),
('Алиса', 'Журавлёва', 'Офтальмолог', 'LIC-105-2026', '+7-910-555-1005', 'alisa.zhuravleva@medlife.ru', 12),
('Тимофей', 'Иваненко', 'Эндокринолог', 'LIC-106-2026', '+7-910-555-1006', 'timofey.ivanenko@medlife.ru', 7),
('Майя', 'Колосова', 'Гастроэнтеролог', 'LIC-107-2026', '+7-910-555-1007', 'maya.kolosova@medlife.ru', 10),
('Глеб', 'Лебедев', 'Дерматолог', 'LIC-108-2026', '+7-910-555-1008', 'gleb.lebedev@medlife.ru', 8);

-- Пациенты (менее распространённые сочетания)
INSERT INTO patients (first_name, last_name, birth_date, phone, email, insurance_number) VALUES
('Савелий', 'Верещагин', '1988-07-14', '+7-920-666-2001', 'saveliy.vereshagin@mail.ru', 'INS-A100-2026'),
('Любава', 'Орехова', '1992-11-02', '+7-920-666-2002', 'lyubava.orekhova@mail.ru', 'INS-A101-2026'),
('Мирослав', 'Печерский', '1980-03-25', '+7-920-666-2003', 'miroslav.pechersky@mail.ru', 'INS-A102-2026'),
('Злата', 'Рябинина', '1995-09-17', '+7-920-666-2004', 'zlata.ryabinina@mail.ru', 'INS-A103-2026'),
('Демид', 'Серебров', '1975-05-30', '+7-920-666-2005', 'demid.serebrov@mail.ru', 'INS-A104-2026'),
('Ярослава', 'Туманова', '1990-12-22', '+7-920-666-2006', 'yaroslava.tumanova@mail.ru', 'INS-A105-2026'),
('Артемий', 'Устинов', '1983-08-08', '+7-920-666-2007', 'artemiy.ustinov@mail.ru', 'INS-A106-2026'),
('Веселина', 'Федосеева', '1997-04-11', '+7-920-666-2008', 'veselina.fedoseeva@mail.ru', 'INS-A107-2026'),
('Радомир', 'Холодов', '1979-01-29', '+7-920-666-2009', 'radomir.kholodov@mail.ru', 'INS-A108-2026'),
('Светозара', 'Чеботарёва', '1993-06-06', '+7-920-666-2010', 'svetozara.chebotareva@mail.ru', 'INS-A109-2026');

-- Приёмы (даты приближены к 4 мая 2026)
INSERT INTO appointments (patient_id, doctor_id, appointment_date, appointment_time, status, diagnosis, prescription, notes) VALUES
(1, 1, '2026-05-04', '09:00', 'completed', 'Острый фарингит', 'Полоскание ромашкой, леденцы Стрепсилс', 'Температура 37.2, общее недомогание'),
(2, 2, '2026-05-04', '10:00', 'completed', 'Гипертоническая болезнь I ст.', 'Эналаприл 5 мг утром', 'Рекомендован контроль давления ежедневно'),
(3, 3, '2026-05-04', '11:00', 'completed', 'Мигрень без ауры', 'Суматриптан 50 мг при приступе', 'Избегать стрессов, нормализовать сон'),
(4, 4, '2026-05-03', '09:30', 'completed', 'Дорсопатия поясничного отдела', 'Диклофенак гель местно, ЛФК', 'Ограничение физических нагрузок на 2 недели'),
(5, 5, '2026-05-03', '10:30', 'completed', 'Конъюнктивит бактериальный', 'Ципрофлоксацин капли 4 р/д', 'Не носить контактные линзы до выздоровления'),
(6, 6, '2026-05-03', '11:30', 'completed', 'Сахарный диабет 2 типа (впервые выявленный)', 'Метформин 500 мг 2 р/д', 'Консультация диетолога, контроль глюкозы'),
(7, 7, '2026-05-02', '09:00', 'completed', 'Хронический гастрит, обострение', 'Омепразол 20 мг утром, диета №1', 'Исключить острое, жареное, алкоголь'),
(8, 8, '2026-05-02', '10:00', 'completed', 'Атопический дерматит', 'Крем с гидрокортизоном, эмоленты', 'Увлажнение кожи после душа'),
(9, 1, '2026-05-02', '11:00', 'cancelled', NULL, NULL, 'Пациент отменил запись по семейным обстоятельствам'),
(10, 2, '2026-05-01', '09:00', 'no_show', NULL, NULL, 'Не явился, телефон недоступен'),
(1, 3, '2026-05-01', '10:00', 'completed', 'Невралгия тройничного нерва', 'Карбамазепин 200 мг 2 р/д', 'Повторный приём через 14 дней'),
(2, 4, '2026-04-30', '12:00', 'completed', 'Плантарный фасциит', 'Ортопедические стельки, НПВС', 'Ограничить ходьбу на каблуках'),
(3, 5, '2026-04-30', '13:00', 'completed', 'Катаракта начальная', 'Капли Квинакс, наблюдение', 'Контроль через 6 месяцев'),
(4, 6, '2026-04-29', '10:00', 'completed', 'Тиреоидит аутоиммунный', 'L-тироксин 50 мкг', 'Контроль ТТГ через 3 месяца'),
(5, 7, '2026-04-29', '11:00', 'completed', 'Язвенная болезнь желудка', 'Амоксициллин, кларитромицин, омепразол', 'Эрадикационная терапия 14 дней'),
(6, 8, '2026-04-28', '09:00', 'completed', 'Экзема кистей', 'Мазь с мометазоном', 'Избегать контакта с моющими средствами без перчаток'),
(7, 1, '2026-05-05', '09:00', 'scheduled', NULL, NULL, 'Плановый осмотр после лечения'),
(8, 3, '2026-05-05', '10:00', 'scheduled', NULL, NULL, 'Контроль неврологического статуса'),
(9, 5, '2026-05-06', '11:00', 'scheduled', NULL, NULL, 'Проверка остроты зрения'),
(10, 7, '2026-05-06', '12:00', 'scheduled', NULL, NULL, 'Гастроскопия контрольная');