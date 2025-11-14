RemoteCoach API - Global Solution
=====================================

**Nome:** Alexsandro Macedo  
**RM:** 557068

## Descrição do Projeto

Este projeto foi desenvolvido como parte da **Global Solution (GS)**, apresentando uma API FastAPI para chatbot especializado em trabalho remoto e produtividade. O sistema integra com a API da Groq (LLM) e mantém histórico de conversas em banco SQLite, oferecendo orientações personalizadas sobre equilíbrio vida pessoal/profissional em regime híbrido.

## Funcionalidades

- ✅ **Endpoint REST** para chat com IA especializada
- ✅ **Integração com Groq** (modelo Llama 3.1 8B)
- ✅ **Persistência de dados** em SQLite
- ✅ **Documentação automática** via FastAPI/Swagger
- ✅ **Configuração via variáveis de ambiente**

## Requisitos

- Python 3.11+
- Virtualenv (recomendado)
- Conta e chave de API da Groq (`https://console.groq.com/`)

## Configuração do Ambiente

1. **Clone e navegue para o diretório:**
   ```bash
   cd chatbot-iot
   ```

2. **Crie e ative o ambiente virtual:**
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. **Instale as dependências:**
   ```powershell
   python -m pip install -r requirements.txt
   ```

4. **Configure as variáveis de ambiente:**
   ```powershell
   Copy-Item .env.example .env
   # Edite o arquivo .env e preencha sua chave API da Groq
   ```

## Variáveis de Ambiente

Configure no arquivo `.env`:

```env
AI_API_KEY=sua_chave_groq_aqui
AI_API_URL=https://api.groq.com/openai/v1/chat/completions
AI_MODEL_NAME=llama-3.1-8b-instant
AI_TEMPERATURE=0.7
AI_MAX_TOKENS=512
```

## Execução da Aplicação

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

A API estará disponível em: `http://127.0.0.1:8000`

## Documentação da API

Acesse a documentação interativa em: `http://127.0.0.1:8000/docs`

## Testando com Insomnia/Postman

**Endpoint Principal:**
- **URL:** `http://127.0.0.1:8000/chat`
- **Método:** `POST`
- **Headers:** `Content-Type: application/json`
- **Body (JSON):**
  ```json
  {
    "user_id": 1,
    "message": "Como posso melhorar meu foco trabalhando de casa?"
  }
  ```

**Resposta Esperada (200 OK):**
```json
{
  "answer": "Para melhorar seu foco em home office, recomendo..."
}
```

## Estrutura do Projeto

```
chatbot-iot/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI app e rotas
│   ├── models.py        # Modelos Pydantic
│   ├── ai_client.py     # Cliente para API Groq
│   └── db.py           # Conexão e operações SQLite
├── .env                # Variáveis de ambiente
├── .env.example        # Template de configuração
├── requirements.txt    # Dependências Python
├── chatbot.db         # Banco SQLite (criado automaticamente)
└── README.md          # Este arquivo
```

## Tecnologias Utilizadas

- **FastAPI** - Framework web moderno para Python
- **Uvicorn** - Servidor ASGI para aplicações Python
- **HTTPx** - Cliente HTTP assíncrono
- **Python-dotenv** - Carregamento de variáveis de ambiente
- **SQLite** - Banco de dados local para histórico
- **Groq API** - Serviço de LLM (Llama 3.1)

## Contexto da Global Solution

Este projeto demonstra a aplicação de tecnologias emergentes (IA/LLM) na solução de problemas reais do mercado de trabalho moderno, especificamente:

- **Problema:** Dificuldade de adaptação ao trabalho remoto/híbrido
- **Solução:** Chatbot especializado com orientações personalizadas
- **Impacto:** Melhoria na produtividade e qualidade de vida profissional

## Desenvolvimento e Testes

Para desenvolvimento com reload automático:
```powershell
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Para verificar o histórico de conversas:
- O banco `chatbot.db` é criado automaticamente
- Visualize com qualquer cliente SQLite
- Tabela: `chat_history`

## Possíveis Melhorias Futuras

- [ ] Autenticação JWT para usuários
- [ ] Cache Redis para respostas frequentes
- [ ] Análise de sentimento das mensagens
- [ ] Dashboard para métricas de uso
- [ ] Deploy em cloud (AWS/Azure/GCP)

---
**Alexsandro Macedo - RM: 557068**  
**Global Solution - 2025**