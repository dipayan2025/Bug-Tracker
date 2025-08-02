from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException, status
from beanie.operators import In
from typing import List, Optional
from datetime import datetime

from app.models.bug import Bug, Comment
from app.schemas.bug import AttachmentSchema, BugCreate, BugOut, BugUpdate, CommentCreate, CommentOut, CommentSchema
from app.core.dependencies import get_current_user, get_current_active_user
from app.models.user import User

router = APIRouter(prefix="/bugs", tags=["Bugs"])


@router.post("/", response_model=BugOut)
async def create_bug(
    bug: BugCreate,
    current_user: User = Depends(get_current_active_user)
):
    new_bug = Bug(
        title=bug.title,
        description=bug.description,
        severity=bug.severity,
        status="open",
        reporter_id=str(current_user.id),
        assignee_id=bug.assignee_id,
        comments=[],
        attachments=[]
    )
    await new_bug.insert()

    return BugOut(
        id=str(new_bug.id),
        title=new_bug.title,
        description=new_bug.description,
        status=new_bug.status,
        severity=new_bug.severity,
        reporter_id=new_bug.reporter_id,
        assignee_id=new_bug.assignee_id,
        created_at=new_bug.created_at,
        updated_at=new_bug.updated_at,
        comments=[],
        attachments=[]
    )





@router.get("/", response_model=List[BugOut])
async def list_bugs(
    current_user: User = Depends(get_current_active_user),
    status: Optional[str] = None,
    severity: Optional[str] = None,
    assignee_id: Optional[str] = None
):
    filters = {}

    if status:
        filters["status"] = status
    if severity:
        filters["severity"] = severity
    if assignee_id:
        filters["assignee_id"] = assignee_id

    bugs = await Bug.find(filters).to_list()

    return [
        BugOut(
            id=str(b.id),
            title=b.title,
            description=b.description,
            status=b.status,
            severity=b.severity,
            reporter_id=b.reporter_id,
            assignee_id=b.assignee_id,
            created_at=b.created_at,
            updated_at=b.updated_at,
            comments=[CommentSchema(**c.model_dump()) for c in b.comments],
            attachments=[AttachmentSchema(**a.model_dump()) for a in b.attachments]
        )
        for b in bugs
    ]

  



@router.get("/{bug_id}", response_model=BugOut)
async def get_bug(
    bug_id: str,
    current_user: User = Depends(get_current_active_user)
):
    bug = await Bug.get(bug_id)
    if not bug:
        raise HTTPException(status_code=404, detail="Bug not found")
    return BugOut(
    id=str(bug.id),
    title=bug.title,
    description=bug.description,
    status=bug.status,
    severity=bug.severity,
    reporter_id=bug.reporter_id,
    assignee_id=bug.assignee_id,
    created_at=bug.created_at,
    updated_at=bug.updated_at,
    comments=[CommentSchema(**c.model_dump()) for c in bug.comments],
    attachments=[AttachmentSchema(**a.model_dump()) for a in bug.attachments]
)


@router.patch("/{bug_id}", response_model=BugOut)
async def update_bug(
    bug_id: str,
    update: BugUpdate,
    current_user: User = Depends(get_current_active_user)
):
    bug = await Bug.get(bug_id)
    if not bug:
        raise HTTPException(status_code=404, detail="Bug not found")

    if update.status:
        bug.status = update.status
    if update.assignee_id:
        bug.assignee_id = update.assignee_id

    bug.updated_at = datetime.utcnow()
    await bug.save()
    return BugOut(
        id=str(bug.id),
        title=bug.title,
        description=bug.description,
        status=bug.status,
        severity=bug.severity,
        reporter_id=bug.reporter_id,
        assignee_id=bug.assignee_id,
        created_at=bug.created_at,
        updated_at=bug.updated_at,
        comments=bug.comments,
        attachments=bug.attachments,
    )

from fastapi.responses import JSONResponse

@router.post("/{bug_id}/comments")
async def add_comment(
    bug_id: str,
    comment: CommentCreate,
    current_user: User = Depends(get_current_active_user)
):
    bug = await Bug.get(PydanticObjectId(bug_id))
    if not bug:
        raise HTTPException(status_code=404, detail="Bug not found")

    new_comment = Comment(
        commenter_id=str(current_user.id),
        text=comment.text,
        timestamp=datetime.utcnow()
    )

    bug.comments.append(new_comment)
    bug.updated_at = datetime.utcnow()
    await bug.save()

    return JSONResponse(
        status_code=201,
        content={"message": "✅ Comment added successfully."}
    )


