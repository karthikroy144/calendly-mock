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
    assert len(data["available_slots"]) > 0


def test_booking_makes_slot_unavailable():
    payload = {
        "patient_name": "Test User",
        "appointment_type": "consultation",
        "date": "2026-01-11",
        "start_time": "09:00"
    }

    first = client.post("/api/calendly/book", json=payload)
    assert first.status_code == 200

    second = client.post("/api/calendly/book", json=payload)
    assert second.status_code == 409
