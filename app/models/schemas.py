from pydantic import BaseModel
from typing import List

class Slot(BaseModel):
    start: str
    end: str

class AvailabilityResponse(BaseModel):
    date: str
    appointment_type: str
    duration_minutes: int
    available_slots: List[Slot]

class BookingRequest(BaseModel):
    patient_name: str
    appointment_type: str
    date: str
    start_time: str

class BookingResponse(BaseModel):
    status: str
    booking_id: str
    message: str