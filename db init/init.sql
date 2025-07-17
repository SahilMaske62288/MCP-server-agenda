

-- Create tables
CREATE TABLE patients (
    id TEXT PRIMARY KEY,
    patient_name TEXT NOT NULL,
    patient_address TEXT,
    patient_phonenumber TEXT
);

CREATE TABLE appointment_types (
    id SERIAL PRIMARY KEY,
    appointment_type TEXT NOT NULL,
    hourly_rate DECIMAL(10, 2)
);

CREATE TABLE agenda (
    id SERIAL PRIMARY KEY,
    patient_id TEXT REFERENCES patients(id),
    appointment_id INT REFERENCES appointment_types(id),
    appointment_date DATE NOT NULL,
    start_hour TIME NOT NULL,
    end_hour TIME NOT NULL
);



-- push data into tables


-- Import data from CSV into patients table
-- id, name, address, phone
COPY patients(id, patient_name, patient_address, patient_phonenumber)
FROM '/csv/patients.csv'
DELIMITER ','
CSV HEADER;

-- Import data from CSV into appointment_types table
-- id, type_name, duration_minutes, cost
COPY appointment_types(id, appointment_type, hourly_rate)
FROM '/csv/appointment_type.csv'
DELIMITER ','
CSV HEADER;

-- Import data from CSV into agenda table
-- id, patient_id, appointment_id, appointment_date, start_hour, end_hour
COPY agenda(id, patient_id, appointment_id, appointment_date, start_hour, end_hour)
FROM '/csv/appointments.csv'
DELIMITER ','
CSV HEADER;