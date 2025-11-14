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


async def ask_remote_coach(user_message: str) -> str:
    if not AI_API_KEY:
        raise RuntimeError("AI_API_KEY não configurada no .env")

    payload = {
        "model": AI_MODEL_NAME,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
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
