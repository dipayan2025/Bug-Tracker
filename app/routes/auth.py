from fastapi import APIRouter, HTTPException, status, Depends
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserOut
from app.core.security import hash_password, verify_password
from app.core.jwt import create_access_token

router = APIRouter(tags=["Auth"])



@router.post("/register", response_model=UserOut)
async def register_user(user: UserCreate):
    if await User.find_one({"email": user.email}):
        raise HTTPException(400, "Email already registered")
    new_user = User(
        email=user.email,
        username=user.username,
        password=hash_password(user.password),
    )
    await new_user.insert()

    
    payload = new_user.dict(exclude={"id", "_id"})
    return UserOut(**payload, id=str(new_user.id))


@router.post("/login")
async def login(user: UserLogin):
    try:
        db_user = await User.find_one(User.email == user.email)
        if not db_user or not verify_password(user.password, db_user.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        token = create_access_token({
            "sub": str(db_user.id),
            "role": db_user.role
        })
        return {"access_token": token, "token_type": "bearer"}
    except Exception as e:
        print(f"⚠️ Login error: {e}")
        raise HTTPException(status_code=500, detail="Login failed")

