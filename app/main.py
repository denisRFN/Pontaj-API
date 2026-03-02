from fastapi import FastAPI
from sqlalchemy import text
from app.database import init_db, engine
from app.routers import hours, calendar, auth

app = FastAPI(
    title="Pontaj API Production",
    version="1.0.0"
)


@app.on_event("startup")
def on_startup():
    init_db()

    with engine.connect() as conn:
        conn.execute(text("""
            ALTER TABLE hours
            ADD COLUMN IF NOT EXISTS overtime_hours INTEGER DEFAULT 0;
        """))

        conn.execute(text("""
            ALTER TABLE hours
            ADD COLUMN IF NOT EXISTS leave_hours INTEGER DEFAULT 0;
        """))

        conn.commit()


app.include_router(hours.router)
app.include_router(calendar.router)
app.include_router(auth.router)
