from pydantic import BaseModel
from typing import List, Optional

class Document(BaseModel):
    id: str
    title: str
    content: str
    tags: Optional[List[str]] = None
    created_at: str
    updated_at: str

class DocumentCreate(BaseModel):
    title: str
    content: str
    tags: Optional[List[str]] = None

class DocumentUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[List[str]] = None