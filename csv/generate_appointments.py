import pandas as pd
import random
from datetime import datetime, timedelta
from faker import Faker
fake= Faker()

# Patient numbers and appointment types
# ---- Generate 100 patients ----
patients = []
for i in range(1, 101):
    patient_number = f'P{str(i).zfill(3)}'
    name = fake.name()
    address = fake.address().replace('\n', ', ')
    phone = fake.phone_number()
    patients.append({
        'id': i,
        'patient_number': patient_number,
        'patient_name': name,
        'patient_address': address,
        'patient_phonenumber': phone
    })
df_patients = pd.DataFrame(patients)
df_patients.to_csv("patients.csv", index=False)
print("Generated patients.csv")

appointment_types = {
    100: 'General Consultation',
    75: 'Follow-up Visit',
    120: 'Physical Exam',
    50: 'Vaccination',
    150: 'Therapy Session',
    00: 'Emergency Appointment',
    30: 'Specialist Consultation',
    200: 'Surgery Consultation',
    90: 'Lab Test Review',
    60: 'Medication Review'
}

df_apt_types = pd.DataFrame([
    {'appointment_number': k, 'appointment_name': v}
    for k, v in appointment_types.items()
])
df_apt_types['hourly_rate'] = [70, 50, 80, 40, 100, 500, 60, 120, 30, 40]
df_apt_types.to_csv("appointment_type.csv", index=False)
print("Generated appointment_type.csv")

# Generate 500 appointments
appointments = []
appointment_type_list = list(appointment_types.keys())
start_date = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)

i = 0
while len(appointments) < 500:
    patient = random.choice(patients)
    apt_type = random.choice(appointment_type_list)

    # Random datetime in next 4 months
    days_offset = random.randint(0, 120)
    hour = random.randint(8, 17)  # Work hours: 8 AM - 5 PM
    minute = random.choice([0, 15, 30, 45])
    start_time = start_date + timedelta(days=days_offset, hours=hour, minutes=minute)
    
    # Skip if it's a weekend (5 = Saturday, 6 = Sunday)
    if start_time.weekday() in [5, 6]:
        continue
        
    duration = random.choice([15, 30, 45, 60])  # in minutes
    end_time = start_time + timedelta(minutes=duration)

    appointments.append({
        "id": i,
        "patient_number": patient.get('patient_number'),
        "appointment_type": apt_type,
        "appointment_date": start_time.strftime('%Y-%m-%d'),
        "start_hour": start_time.strftime('%H:%M'),
        "end_hour": end_time.strftime('%H:%M')
    })
    i += 1

# Save to CSV
df = pd.DataFrame(appointments)
df.to_csv("appointments.csv", index=False)
print("Generated appointments.csv")
