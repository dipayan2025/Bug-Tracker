from fastapi import APIRouter, Depends, HTTPException, status
from beanie.operators import In
from typing import List, Optional
from datetime import datetime

from app.models.bug import Bug, Comment
from app.schemas.bug import BugCreate, BugOut, BugUpdate, CommentCreate
from app.core.dependencies import get_current_user, get_current_active_user
from app.models.user import User

router = APIRouter(prefix="/bugs", tags=["Bugs"])

# 🐞 Create new bug report
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
    
    # Convert to response format
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

# 📋 List bugs with optional filters
@router.get("/", response_model=List[BugOut])
async def list_bugs(
    status: Optional[str] = None,
    severity: Optional[str] = None,
    assignee_id: Optional[str] = None,
    current_user: User = Depends(get_current_active_user)
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


@router.get("/{bug_id}", response_model=BugOut)
async def get_bug(
    bug_id: str,
    current_user: User = Depends(get_current_active_user)
):
    bug = await Bug.get(bug_id)
    if not bug:
        raise HTTPException(status_code=404, detail="Bug not found")
    return bug

# ✏️ Update bug (status or assign)
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
    return bug

# 💬 Add comment to a bug
@router.post("/{bug_id}/comments", response_model=BugOut)
async def add_comment(
    bug_id: str,
    comment: CommentCreate,
    current_user: User = Depends(get_current_active_user)
):
    bug = await Bug.get(bug_id)
    if not bug:
        raise HTTPException(status_code=404, detail="Bug not found")

    new_comment = Comment(
        commenter_id=str(current_user.id),
        text=comment.content,
        timestamp=datetime.utcnow()
    )
    bug.comments.append(new_comment)
    bug.updated_at = datetime.utcnow()
    await bug.save()
    return bug
