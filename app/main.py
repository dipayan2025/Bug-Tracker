from fastapi import FastAPI
from app.database import init_db
app=FastAPI()


@app.on_event("startup")
async def start_db():
    await init_db()

