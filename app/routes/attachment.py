import shutil
from beanie import PydanticObjectId
from fastapi import Depends, UploadFile, File, HTTPException
import os
from uuid import uuid4
from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app.models.user import User
from app.schemas import bug
from app.schemas.user import UserCreate, UserLogin, UserOut, Token
from app.core.dependencies import get_current_active_user
from app.models.bug import Attachment, Bug
from app.schemas.bug import BugOut
router = APIRouter(prefix="/attachments", tags=["Attachments"])
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/{bug_id}/attachments", response_model=BugOut)
async def upload_file(
    bug_id: str,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user)
):
    bug = await Bug.get(PydanticObjectId(bug_id))
    if not bug:
        raise HTTPException(status_code=404, detail="Bug not found")

    # Validate size (max 5MB)
    contents = await file.read()
    max_size = 5 * 1024 * 1024
    if len(contents) > max_size:
        raise HTTPException(status_code=400, detail="File too large")

    # Validate type
    allowed_types = ["image/png", "image/jpeg", "application/pdf"]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Invalid file type")

    # Save to disk
    filename = f"{uuid4().hex}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    with open(file_path, "wb") as f:
        f.write(contents)

    attachment = Attachment(
        filename=file.filename,
        content_type=file.content_type,
        size=len(contents),
        uploaded_at=datetime.utcnow(),
        uploader_id=str(current_user.id),
        url=f"/api/files/{filename}"
    )
    bug.attachments.append(attachment)
    bug.updated_at = datetime.utcnow()
    await bug.save()
    
    bug_dict = bug.dict()
    bug_dict["id"] = str(bug.id)
    return BugOut(**bug_dict)


from fastapi.responses import FileResponse

@router.get("/files/{filename}")
async def download_file(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path)
