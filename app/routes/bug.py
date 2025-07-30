from fastapi import APIRouter, Depends, HTTPException, status
from beanie.operators import In
from typing import List, Optional
from datetime import datetime

from app.models.bug import Bug, Comment
from app.schemas.bug import BugCreate, BugOut, BugUpdate, CommentCreate
from app.core.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/bugs", tags=["Bugs"])

# 🐞 Create new bug report
@router.post("/", response_model=BugOut)
async def create_bug(
    bug: BugCreate,
    current_user: User = Depends(get_current_user)
):
    new_bug = Bug(
        title=bug.title,
        description=bug.description,
        severity=bug.severity,
        status="open",  # optional default
        reporter_id=str(current_user.id),
        assignee_id=None,
        comments=[],
        attachments=[]
    )
    await new_bug.insert()

    # ✅ Ensure correct response structure
    payload = new_bug.dict(exclude={"id", "_id"})
    return BugOut(**payload, id=str(new_bug.id))

# 📋 List bugs with optional filters
@router.get("/", response_model=List[BugOut])
async def list_bugs(
    status: Optional[str] = None,
    severity: Optional[str] = None,
    assignee_id: Optional[str] = None,
):
    filters = {}
    if status:
        filters["status"] = status
    if severity:
        filters["severity"] = severity
    if assignee_id:
        filters["assignee_id"] = assignee_id

    bugs = await Bug.find(filters).to_list()
    return bugs

# 🔍 Get bug details
@router.get("/{bug_id}", response_model=BugOut)
async def get_bug(bug_id: str):
    bug = await Bug.get(bug_id)
    if not bug:
        raise HTTPException(status_code=404, detail="Bug not found")
    return bug

# ✏️ Update bug (status or assign)
@router.patch("/{bug_id}", response_model=BugOut)
async def update_bug(
    bug_id: str,
    update: BugUpdate,
    current_user: User = Depends(get_current_user)
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
    return bug

# 💬 Add comment to a bug
@router.post("/{bug_id}/comments", response_model=BugOut)
async def add_comment(
    bug_id: str,
    comment: CommentCreate,
    current_user: User = Depends(get_current_user)
):
    bug = await Bug.get(bug_id)
    if not bug:
        raise HTTPException(status_code=404, detail="Bug not found")

    new_comment = Comment(
        author_id=str(current_user.id),
        content=comment.content,
    )
    bug.comments.append(new_comment)
    bug.updated_at = datetime.utcnow()
    await bug.save()
    return bug
