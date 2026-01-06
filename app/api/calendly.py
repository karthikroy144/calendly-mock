from fastapi import APIRouter, HTTPException, Query
from uuid import uuid4
from datetime import datetime
from app.config import APPOINTMENT_TYPES
from app.services.scheduler import get_available_slots, book_slot
from app.models.schemas import AvailabilityResponse, BookingRequest, BookingResponse, Slot

router = APIRouter()

@router.get("/availability", response_model=AvailabilityResponse)
def availability(date: str = Query(...), appointment_type: str = Query(...)):
    if appointment_type not in APPOINTMENT_TYPES:
        raise HTTPException(400, "Invalid appointment type")

    slots = get_available_slots(date, appointment_type)
    return AvailabilityResponse(
        date=date,
        appointment_type=appointment_type,
        duration_minutes=APPOINTMENT_TYPES[appointment_type],
        available_slots=[Slot(**s) for s in slots]
    )

@router.post("/book", response_model=BookingResponse)
def book(payload: BookingRequest):
    slots = get_available_slots(payload.date, payload.appointment_type)
    if not any(s["start"] == payload.start_time for s in slots):
        raise HTTPException(409, "Slot not available")

    book_slot(payload.date, payload.appointment_type, payload.patient_name, payload.start_time)

    return BookingResponse(
        status="confirmed",
        booking_id=f"bk_{uuid4().hex[:8]}",
        message="Appointment successfully booked"
    )