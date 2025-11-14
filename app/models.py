from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    user_id: int = Field(..., example=1)
    message: str = Field(..., example="Como melhorar meu foco em home office?")

class ChatResponse(BaseModel):
    answer: str
