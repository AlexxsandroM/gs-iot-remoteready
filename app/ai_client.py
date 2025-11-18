import os
import httpx
from dotenv import load_dotenv

# Força reload do .env sobrescrevendo variáveis existentes
load_dotenv(override=True)

def _get_env_float(var_name: str, default: float) -> float:
    value = os.getenv(var_name)
    if value is None:
        return default
    try:
        return float(value)
    except ValueError:
        return default


def _get_env_int(var_name: str, default: int) -> int:
    value = os.getenv(var_name)
    if value is None:
        return default
    try:
        return int(value)
    except ValueError:
        return default


AI_API_KEY = os.getenv("AI_API_KEY")
AI_API_URL = os.getenv("AI_API_URL", "https://api.groq.com/openai/v1/chat/completions")
AI_MODEL_NAME = os.getenv("AI_MODEL_NAME", "llama-3.1-8b-instant")
AI_TEMPERATURE = _get_env_float("AI_TEMPERATURE", 0.7)
AI_MAX_TOKENS = _get_env_int("AI_MAX_TOKENS", 512)

SYSTEM_PROMPT = """
Você é o RemoteCoach, um chatbot especialista em trabalho remoto, produtividade,
organização financeira básica e equilíbrio entre vida pessoal e profissional.
Responda em português do Brasil, de forma simples e objetiva.
"""


def _build_personalized_prompt(user_context: dict = None) -> str:
    """Constrói um prompt personalizado baseado no contexto do usuário"""
    if not user_context:
        return SYSTEM_PROMPT
    
    personalized = SYSTEM_PROMPT + "\n\n=== CONTEXTO DO USUÁRIO ===\n"
    
    if user_context.get('nome'):
        personalized += f"Nome: {user_context['nome']}\n"
    
    if user_context.get('perfil'):
        perfil = user_context['perfil']
        if perfil == 'JUNIOR':
            personalized += "Nível: Júnior (iniciante na carreira)\n"
            personalized += "Dica: Adapte suas respostas para alguém começando, seja mais didático e explique conceitos básicos.\n"
        elif perfil == 'PLENO':
            personalized += "Nível: Pleno (experiência intermediária)\n"
            personalized += "Dica: O usuário já tem conhecimento básico, pode ir direto ao ponto.\n"
        elif perfil == 'SENIOR':
            personalized += "Nível: Sênior (experiência avançada)\n"
            personalized += "Dica: Forneça insights avançados e estratégicos.\n"
    
    if user_context.get('experiencia') is not None:
        anos = user_context['experiencia']
        personalized += f"Experiência: {anos} ano(s) de trabalho\n"
    
    if user_context.get('avaliacao'):
        personalized += f"Avaliação na plataforma: {user_context['avaliacao']:.1f}/5.0\n"
    
    personalized += "\nUse essas informações para personalizar sua resposta de acordo com o perfil e experiência do usuário.\n"
    
    return personalized


async def ask_remote_coach(user_message: str, user_context: dict = None) -> str:
    if not AI_API_KEY:
        raise RuntimeError("AI_API_KEY não configurada no .env")

    system_prompt = _build_personalized_prompt(user_context)

    payload = {
        "model": AI_MODEL_NAME,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        "temperature": AI_TEMPERATURE,
        "max_tokens": AI_MAX_TOKENS,
        "stream": False,
    }

    headers = {
        "Authorization": f"Bearer {AI_API_KEY}",
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient(timeout=30) as client:
        try:
            resp = await client.post(AI_API_URL, json=payload, headers=headers)
            resp.raise_for_status()
        except httpx.HTTPStatusError as exc:
            detail = exc.response.text[:500]
            raise RuntimeError(
                f"Groq retornou {exc.response.status_code}: {detail}"
            ) from exc

    data = resp.json()

    try:
        message = data["choices"][0]["message"]
        answer = message.get("content") or message.get("reasoning_content")
    except (KeyError, IndexError, AttributeError) as exc:
        raise RuntimeError("Resposta inesperada recebida da API Groq") from exc

    if not answer:
        raise RuntimeError("Resposta vazia recebida da API Groq")

    return answer.strip()
