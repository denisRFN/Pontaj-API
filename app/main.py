from fastapi import FastAPI
from app.database import init_db
from app.routers import hours, calendar
from app.models import user
app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(hours.router)
app.include_router(calendar.router)

