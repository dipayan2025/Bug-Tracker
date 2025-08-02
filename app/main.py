from fastapi import FastAPI
from app.database import init_db
from app.routes import auth, user, bug, attachment

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await init_db()

app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(user.router, prefix="/api/users", tags=["Users"])
app.include_router(bug.router, prefix="/api/bugs", tags=["Bugs"])
app.include_router(attachment.router, prefix="/api/attachments", tags=["Attachments"])