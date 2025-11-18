from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class ChatRequest(BaseModel):
    user_id: int = Field(..., example=1)
    message: str = Field(..., example="Como melhorar meu foco em home office?")

class ChatResponse(BaseModel):
    answer: str

class ChatHistoryItem(BaseModel):
    id: int
    prompt: str
    response: str
    created_at: datetime

class ChatHistoryResponse(BaseModel):
    history: List[ChatHistoryItem]
