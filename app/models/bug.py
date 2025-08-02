from beanie import Document
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Comment(BaseModel):
    commenter_id: str
    text: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class Attachment(BaseModel):
    filename: str
    content_type: str
    size: int  # in bytes
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)
    uploader_id: str
    url: str
    
  
#class CommentCreate(BaseModel):
    #text: str



#class CommentOut(BaseModel):  # for response
   # commenter_id: str
   # text: str
    #timestamp: datetime



class Bug(Document):
    title: str
    description: str
    status: str = "open" 
    severity: str = "low"  
    reporter_id: str
    assignee_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    comments: List[Comment]
    attachments: List[Attachment] 

    class Settings:
        name = "bugs"

    class Config:
        schema_extra = {
            "example": {
                "title": "Login issue",
                "description": "Unable to login with valid credentials.",
                "status": "open",
                "severity": "high",
                "reporter_id": "user123"
            }
        }
