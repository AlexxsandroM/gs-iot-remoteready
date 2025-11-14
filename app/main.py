from fastapi import FastAPI, HTTPException
from .models import ChatRequest, ChatResponse
from .ai_client import ask_remote_coach
from .db import init_db, save_message

app = FastAPI(
    title="RemoteCoach - Chatbot IoT/IA",
    description="API em Python para chatbot de equilíbrio vida pessoal/profissional em regime híbrido.",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_event():
    init_db()

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(payload: ChatRequest):
    try:
        bot_answer = await ask_remote_coach(payload.message)
    except Exception as e:
        # Aqui você pode logar o erro de forma mais detalhada
        raise HTTPException(status_code=500, detail=f"Erro ao consultar IA: {e}")

    # Salva no histórico
    save_message(payload.user_id, payload.message, bot_answer)

    return ChatResponse(answer=bot_answer)
