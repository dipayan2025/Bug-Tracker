

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import FileResponse
from uuid import uuid4
import os
import shutil

from app.config import settings
from app.models.bug import Bug, Attachment
from app.core.dependencies import get_current_active_user
from app.schemas.bug import AttachmentSchema  

router = APIRouter(prefix="/attachments", tags=["Attachments"])

@router.post("/upload/{bug_id}")
async def upload_attachment(
    bug_id: str,
    file: UploadFile = File(...),
    current_user=Depends(get_current_active_user)
):
    if file.content_type not in settings.ALLOWED_FILE_TYPES:
        raise HTTPException(status_code=400, detail="Invalid file type")

    contents = await file.read()
    if len(contents) > settings.MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large")
    
    await file.seek(0)

    extension = file.filename.split(".")[-1]
    unique_name = f"{uuid4()}.{extension}"
    full_path = os.path.join(settings.UPLOAD_DIR, unique_name)

    with open(full_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    bug = await Bug.get(bug_id)
    if not bug:
        raise HTTPException(status_code=404, detail="Bug not found")

    attachment = Attachment(
        filename=file.filename,
        filepath=full_path,
        content_type=file.content_type,
        size=len(contents)
    )

    bug.attachments.append(attachment)
    await bug.save()

    return {"message": "Attachment uploaded successfully", "filename": file.filename}


@router.get("/download/{bug_id}/{filename}")
async def download_attachment(
    bug_id: str,
    filename: str,
    current_user=Depends(get_current_active_user)
):
    bug = await Bug.get(bug_id)
    if not bug:
        raise HTTPException(status_code=404, detail="Bug not found")

    attachment = next((a for a in bug.attachments if a.filename == filename), None)
    if not attachment:
        raise HTTPException(status_code=404, detail="Attachment not found")

    return FileResponse(
        path=attachment.filepath,
        filename=attachment.filename,
        media_type=attachment.content_type or "application/octet-stream"
    )



@router.get("/list/{bug_id}", response_model=list[AttachmentSchema])
async def list_attachments(
    bug_id: str,
    current_user=Depends(get_current_active_user)
):
    bug = await Bug.get(bug_id)
    if not bug:
        raise HTTPException(status_code=404, detail="Bug not found")

    return [
        AttachmentSchema(
            **a.model_dump(),
            download_url=f"/attachments/download/{str(bug.id)}/{a.filename}"
        )
        for a in bug.attachments
    ]
