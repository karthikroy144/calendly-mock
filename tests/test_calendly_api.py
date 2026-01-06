from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_availability_returns_slots():
    response = client.get(
        "/api/calendly/availability",
        params={
            "date": "2026-01-10",
            "appointment_type": "consultation"
        }
    )

    assert response.status_code == 200

    data = response.json()
    assert data["appointment_type"] == "consultation"
    assert data["duration_minutes"] == 30
    assert isinstance(data["available_slots"], list)
    assert len(data["available_slots"]) > 0


def test_booking_makes_slot_unavailable():
    booking_payload = {
        "patient_name": "Test User",
        "appointment_type": "consultation",
        "date": "2026-01-11",
        "start_time": "09:00"
    }

    # Book the slot
    book_response = client.post(
        "/api/calendly/book",
        json=booking_payload
    )
    assert book_response.status_code == 200

    # Try booking the same slot again
    duplicate_response = client.post(
        "/api/calendly/book",
        json=booking_payload
    )
    assert duplicate_response.status_code == 409
