from fastapi import APIRouter
from app.config import settings
from motor.motor_asyncio import AsyncIOMotorClient

router = APIRouter()

@router.get("/health/db")
async def check_db_connection():
    try:
        client = AsyncIOMotorClient(settings.MONGO_URI)
        # Ping the server
        await client.admin.command("ping")
        return {"status": "✅ Connected to MongoDB"}
    except Exception as e:
        return {"status": "❌ Not connected", "error": str(e)}
