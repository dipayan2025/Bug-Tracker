from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.user import UserOut, UserProfileUpdate, UpdateRoleRequest
from app.models.user import User
from app.core.dependencies import get_current_user, require_manager
from beanie import PydanticObjectId

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=UserOut)
async def get_profile(current_user: User = Depends(get_current_user)):
    return current_user

# ✏️ Update current user's profile
@router.patch("/me", response_model=UserOut)
async def update_profile(update: UserProfileUpdate, current_user: User = Depends(get_current_user)):
    if update.username:
        current_user.username = update.username
    if update.email:
        current_user.email = update.email
    await current_user.save()
    return current_user

# 🔁 Admin: Update any user's role
@router.patch("/{user_id}/role", dependencies=[Depends(require_manager)])
async def update_user_role(
    user_id: str,
    payload: UpdateRoleRequest
):
    user = await User.get(PydanticObjectId(user_id))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.role = payload.role
    await user.save()
    return {"msg": f"Role updated to '{payload.role}'"}

# 🔍 Admin: List all users
@router.get("/", response_model=list[UserOut], dependencies=[Depends(require_manager)])
async def list_users():
    users = await User.find_all().to_list()
    return users
