from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
# app/schemas/bug.py

from pydantic import BaseModel

class CommentCreate(BaseModel):
    content: str

class CommentSchema(BaseModel):
    commenter_id: str
    text: str

class AttachmentSchema(BaseModel):
    filename: str
    filepath: str

class BugCreate(BaseModel):
    title: str
    description: str
    severity: str = "low"
    assignee_id: Optional[str] = None

class BugUpdate(BaseModel):
    status: Optional[str]
    comment: Optional[CommentSchema]

class BugOut(BaseModel):
    id: str
    title: str
    description: str
    status: str
    severity: str
    reporter_id: str
    assignee_id: Optional[str]
    comments: List[CommentSchema]
    attachments: List[AttachmentSchema]
