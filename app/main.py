from fastapi import FastAPI
from app.api.calendly import router as calendly_router

app = FastAPI(title="Mock Calendly Backend")

app.include_router(calendly_router, prefix="/api/calendly")

@app.get("/")
def health():
    return {"status": "ok"}