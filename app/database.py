from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from app.models.user import User
from app.models.bug import Bug
from app.config import settings

async def init_db():
    try:
        client = AsyncIOMotorClient(settings.MONGO_URI)
        await client.admin.command("ping")
        print("✅ MongoDB connected successfully")

        await init_beanie(database=client[settings.DB_NAME], document_models=[User, Bug])
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
