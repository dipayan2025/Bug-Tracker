from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.user import UserOut, UserProfileUpdate, UpdateRoleRequest
from app.models.user import User
from app.core.dependencies import get_current_active_user, get_current_user, require_manager
from beanie import PydanticObjectId

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=UserOut)
async def get_me(current_user: User = Depends(get_current_active_user)):
    return UserOut(
        id=str(current_user.id),
        email=current_user.email,
        username=current_user.username,
        role=current_user.role,
        created_at=current_user.created_at
    )

# ✏️ Update current user's profile
@router.patch("/me", response_model=UserOut)
async def update_my_profile(
    update: UserProfileUpdate,
    current_user: User = Depends(get_current_active_user)
):
    if update.username:
        current_user.username = update.username
    if update.email:
        # Check if the new email is already used by another user
        existing_user = await User.find_one(User.email == update.email)
        if existing_user and existing_user.id != current_user.id:
            raise HTTPException(status_code=400, detail="Email already in use")
        current_user.email = update.email

    await current_user.save()

    return UserOut(
        id=str(current_user.id),
        email=current_user.email,
        username=current_user.username,
        role=current_user.role,
        created_at=current_user.created_at
    )

# 🔁 Admin: Update any user's role
@router.patch("/{user_id}/role", response_model=UserOut, dependencies=[Depends(require_manager)])
async def update_user_role(
    user_id: str,
    role_update: UpdateRoleRequest
):
    user = await User.get(PydanticObjectId(user_id))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.role = role_update.role
    await user.save()

    return UserOut(
        id=str(user.id),
        email=user.email,
        username=user.username,
        role=user.role,
        created_at=user.created_at
    )

# 🔍 Admin: List all users
@router.get("/", response_model=List[UserOut], dependencies=[Depends(require_manager)])
async def list_all_users():
    users = await User.find_all().to_list()
    return [
        UserOut(
            id=str(user.id),
            email=user.email,
            username=user.username,
            role=user.role,
            created_at=user.created_at
        )
        for user in users
    ]