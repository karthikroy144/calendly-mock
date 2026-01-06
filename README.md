# Mock Calendly Backend – Medical Clinic Scheduling

This project implements a **Calendly-like backend scheduling system** for a medical clinic.
It simulates appointment availability and booking logic using **FastAPI**, focusing on clean API design,
time-slot computation, and correctness of business rules.

The implementation is intentionally backend-only, as per the assessment requirements.

---

## 🎯 Objective

Build backend APIs that simulate scheduling logic for a medical clinic, similar to Calendly, with support for:

- Fetching available appointment slots
- Booking appointments with patient data
- Multiple appointment types with different durations
- Prevention of double booking
- Graceful handling of no-availability scenarios

---

## 🛠️ Tech Stack

- **Python**: 3.11 (recommended, compatible with 3.10+)
- **Framework**: FastAPI
- **Validation**: Pydantic
- **Testing**: Pytest + FastAPI TestClient
- **Storage**: In-memory (mock database)

---

## 📁 Project Structure

```
calendly-mock/
│
├── app/
│   ├── main.py               # FastAPI application entry point
│   ├── config.py             # Clinic hours & appointment types
│   │
│   ├── api/
│   │   └── calendly.py       # API routes
│   │
│   ├── services/
│   │   └── scheduler.py     # Slot generation & booking logic
│   │
│   ├── models/
│   │   └── schemas.py       # Pydantic request/response models
│   │
│   └── data/
│       └── mock_db.py       # In-memory booking store
│
├── tests/
│   └── test_calendly_api.py # Minimal API tests
│
├── requirements.txt
└── README.md
```

---

## 🕒 Appointment Types

| Appointment Type | Duration |
|------------------|----------|
| Consultation     | 30 mins  |
| Follow-up        | 15 mins  |
| Therapy          | 60 mins  |

---

## 🚀 Running the Application

### Create and activate virtual environment

```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Start server

```bash
uvicorn app.main:app --reload
```

API base URL:
```
http://127.0.0.1:8000
```

Swagger Docs:
```
http://127.0.0.1:8000/docs
```

---

## 📌 API Endpoints

### Get Availability

```
GET /api/calendly/availability
```

Query Params:
- date (YYYY-MM-DD)
- appointment_type

Example:
```
/api/calendly/availability?date=2026-01-10&appointment_type=consultation
```

Response:
```json
{
  "date": "2026-01-10",
  "appointment_type": "consultation",
  "duration_minutes": 30,
  "available_slots": [
    { "start": "09:00", "end": "09:30" }
  ]
}
```

---

### Book Appointment

```
POST /api/calendly/book
```

Request:
```json
{
  "patient_name": "Rahul Sharma",
  "appointment_type": "consultation",
  "date": "2026-01-10",
  "start_time": "10:00"
}
```

Response:
```json
{
  "status": "confirmed",
  "booking_id": "bk_1a2b3c4d",
  "message": "Appointment successfully booked"
}
```

---

## 🧪 Testing

Run tests:

```bash
pytest -v
```

Tests validate:
- Slot availability logic
- Double booking prevention

---

## 🧠 Design Notes

- Clean separation between API, business logic, and storage
- Deterministic slot generation
- Easily extensible to real databases or Calendly APIs

---

## ⚠️ Limitations

- No authentication
- No persistent database
- Single clinic assumption

---

## 🐍 Python Version

Tested with **Python 3.11** (recommended).
