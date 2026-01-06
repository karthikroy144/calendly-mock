from fastapi import FastAPI
from app.api.calendly import router as calendly_router

app = FastAPI(
    title="Mock Calendly Backend",
    description="Medical clinic scheduling API",
    version="1.0.0"
)

app.include_router(calendly_router, prefix="/api/calendly")


@app.get("/")
def health():
    return {"status": "ok"}
