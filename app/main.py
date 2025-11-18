from fastapi import FastAPI, HTTPException
from .models import ChatRequest, ChatResponse, ChatHistoryResponse
from .ai_client import ask_remote_coach
from .oracle_db import init_oracle_db, save_message_oracle, get_user_history, get_user_info

app = FastAPI(
    title="RemoteCoach - Chatbot IoT/IA",
    description="API em Python para chatbot de equilíbrio vida pessoal/profissional em regime híbrido.",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_event():
    """Inicializa o banco de dados Oracle na inicialização da aplicação"""
    try:
        init_oracle_db()
        print("✅ Banco de dados Oracle inicializado com sucesso!")
    except Exception as e:
        print(f"⚠️ Erro ao inicializar Oracle DB: {e}")
        print("Verifique as configurações de conexão no arquivo .env")

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(payload: ChatRequest):
    """Endpoint principal do chatbot que processa mensagens e salva no Oracle"""
    # Busca informações do usuário para personalizar a resposta
    user_context = None
    try:
        user_context = get_user_info(payload.user_id)
        if not user_context:
            print(f"⚠️ Usuário {payload.user_id} não encontrado na TB_GS_USUARIO")
    except Exception as e:
        print(f"⚠️ Erro ao buscar info do usuário: {e}")
        # Continua sem contexto do usuário
    
    # Gera resposta personalizada da IA
    try:
        bot_answer = await ask_remote_coach(payload.message, user_context)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao consultar IA: {e}")

    # Salva no histórico do Oracle
    try:
        save_message_oracle(payload.user_id, payload.message, bot_answer)
    except Exception as e:
        print(f"⚠️ Erro ao salvar no Oracle: {e}")
        # Continua mesmo com erro ao salvar (opcional: você pode querer lançar exceção aqui)

    return ChatResponse(answer=bot_answer)

@app.get("/chat/history/{user_id}", response_model=ChatHistoryResponse)
async def get_chat_history(user_id: int, limit: int = 10):
    """Retorna o histórico de conversas de um usuário específico"""
    try:
        history = get_user_history(user_id, limit)
        return ChatHistoryResponse(history=history)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar histórico: {e}")
