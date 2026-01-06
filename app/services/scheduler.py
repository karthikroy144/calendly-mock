from datetime import datetime, timedelta
from app.config import CLINIC_START_TIME, CLINIC_END_TIME, APPOINTMENT_TYPES
from app.data.mock_db import BOOKINGS

def generate_slots(date, appointment_type):
    duration = APPOINTMENT_TYPES[appointment_type]
    start = datetime.strptime(f"{date} {CLINIC_START_TIME}", "%Y-%m-%d %H:%M:%S")
    end = datetime.strptime(f"{date} {CLINIC_END_TIME}", "%Y-%m-%d %H:%M:%S")
    slots = []
    while start + timedelta(minutes=duration) <= end:
        s_end = start + timedelta(minutes=duration)
        slots.append({"start": start.strftime("%H:%M"), "end": s_end.strftime("%H:%M")})
        start = s_end
    return slots

def get_available_slots(date, appointment_type):
    booked = BOOKINGS.get(date, [])
    all_slots = generate_slots(date, appointment_type)
    return [s for s in all_slots if s not in booked]

def book_slot(date, appointment_type, patient_name, start_time):
    duration = APPOINTMENT_TYPES[appointment_type]
    start = datetime.strptime(f"{date} {start_time}", "%Y-%m-%d %H:%M")
    end = start + timedelta(minutes=duration)
    BOOKINGS.setdefault(date, []).append({
        "start": start.strftime("%H:%M"),
        "end": end.strftime("%H:%M"),
        "appointment_type": appointment_type,
        "patient_name": patient_name
    })