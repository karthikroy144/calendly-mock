from fastapi import APIRouter, HTTPException, Query
from uuid import uuid4
from datetime import datetime

from app.config import APPOINTMENT_TYPES
from app.services.scheduler import get_available_slots, book_slot
from app.models.schemas import (
    AvailabilityResponse,
    BookingRequest,
    BookingResponse,
    Slot
)

router = APIRouter()


@router.get("/availability", response_model=AvailabilityResponse)
def get_availability(
    date: str = Query(...),
    appointment_type: str = Query(...)
):
    if appointment_type not in APPOINTMENT_TYPES:
        raise HTTPException(status_code=400, detail="Invalid appointment type")

    if datetime.strptime(date, "%Y-%m-%d").date() < datetime.today().date():
        raise HTTPException(status_code=400, detail="Date cannot be in the past")

    available_slots = get_available_slots(date, appointment_type)

    return AvailabilityResponse(
        date=date,
        appointment_type=appointment_type,
        duration_minutes=APPOINTMENT_TYPES[appointment_type],
        available_slots=[Slot(**slot) for slot in available_slots]
    )


@router.post("/book", response_model=BookingResponse)
def book_appointment(payload: BookingRequest):
    if payload.appointment_type not in APPOINTMENT_TYPES:
        raise HTTPException(status_code=400, detail="Invalid appointment type")

    available_slots = get_available_slots(
        payload.date,
        payload.appointment_type
    )

    if not any(slot["start"] == payload.start_time for slot in available_slots):
        raise HTTPException(
            status_code=409,
            detail="Requested slot is not available"
        )

    book_slot(
        date=payload.date,
        appointment_type=payload.appointment_type,
        patient_name=payload.patient_name,
        start_time=payload.start_time
    )

    return BookingResponse(
        status="confirmed",
        booking_id=f"bk_{uuid4().hex[:8]}",
        message="Appointment successfully booked"
    )
