from datetime import datetime, timedelta
from app.config import CLINIC_START_TIME, CLINIC_END_TIME, APPOINTMENT_TYPES
from app.data.mock_db import BOOKINGS


def generate_slots(date: str, appointment_type: str):
    duration = APPOINTMENT_TYPES[appointment_type]
    slots = []

    start_dt = datetime.strptime(
        f"{date} {CLINIC_START_TIME}", "%Y-%m-%d %H:%M:%S"
    )
    end_dt = datetime.strptime(
        f"{date} {CLINIC_END_TIME}", "%Y-%m-%d %H:%M:%S"
    )

    while start_dt + timedelta(minutes=duration) <= end_dt:
        slot_end = start_dt + timedelta(minutes=duration)
        slots.append({
            "start": start_dt.strftime("%H:%M"),
            "end": slot_end.strftime("%H:%M")
        })
        start_dt = slot_end

    return slots


def is_overlapping(slot, booking):
    return not (
        slot["end"] <= booking["start"] or
        slot["start"] >= booking["end"]
    )


def get_available_slots(date: str, appointment_type: str):
    all_slots = generate_slots(date, appointment_type)
    bookings = BOOKINGS.get(date, [])

    available = []
    for slot in all_slots:
        if not any(is_overlapping(slot, booking) for booking in bookings):
            available.append(slot)

    return available


def book_slot(date: str, appointment_type: str, patient_name: str, start_time: str):
    duration = APPOINTMENT_TYPES[appointment_type]
    start_dt = datetime.strptime(f"{date} {start_time}", "%Y-%m-%d %H:%M")
    end_dt = start_dt + timedelta(minutes=duration)

    BOOKINGS.setdefault(date, []).append({
        "start": start_dt.strftime("%H:%M"),
        "end": end_dt.strftime("%H:%M"),
        "appointment_type": appointment_type,
        "patient_name": patient_name
    })
