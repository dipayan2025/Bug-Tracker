from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class CommentCreate(BaseModel):
    text: str

class CommentOut(BaseModel):
    commenter_id: str
    text: str
    timestamp: datetime


class CommentSchema(BaseModel):
    commenter_id: str
    text: str
    timestamp: datetime

class AttachmentSchema(BaseModel):
    filename: str
    filepath: str
    uploaded_at: datetime

class BugCreate(BaseModel):
    title: str
    description: str
    severity: str = "low"
    assignee_id: Optional[str] = None

class BugUpdate(BaseModel):
    status: Optional[str]
    assignee_id: Optional[str]

class BugOut(BaseModel):
    id: str
    title: str
    description: str
    status: str
    severity: str
    reporter_id: str
    assignee_id: Optional[str]
    created_at: datetime
    updated_at: datetime
    comments: List[CommentSchema]
    attachments: List[AttachmentSchema]