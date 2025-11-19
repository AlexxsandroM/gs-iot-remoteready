RemoteCoach API - Global Solution
=====================================

[![Deploy on Render](https://img.shields.io/badge/Deploy-Render-46E3B7?style=flat&logo=render)](https://gs-iot-remoteready.onrender.com/docs)
[![API Status](https://img.shields.io/badge/API-Online-success)](https://gs-iot-remoteready.onrender.com/docs)

**Nome:** Alexsandro Macedo  
**RM:** 557068

**Nome:** Leonardo Salazar  
**RM:** 557484

## 🚀 Acesso Rápido

- **API em Produção:** [https://gs-iot-remoteready.onrender.com](https://gs-iot-remoteready.onrender.com)
- **Documentação Interativa (Swagger):** [https://gs-iot-remoteready.onrender.com/docs](https://gs-iot-remoteready.onrender.com/docs)
- **Documentação Alternativa (ReDoc):** [https://gs-iot-remoteready.onrender.com/redoc](https://gs-iot-remoteready.onrender.com/redoc)

## Descrição do Projeto

Este projeto foi desenvolvido como parte da **Global Solution (GS)**, apresentando uma API FastAPI para chatbot especializado em trabalho remoto e produtividade. O sistema integra com a API da Groq (LLM) e mantém histórico de conversas em banco de dados **Oracle SQL**, oferecendo orientações personalizadas sobre equilíbrio vida pessoal/profissional em regime híbrido.

## Funcionalidades

- ✅ **Endpoint REST** para chat com IA especializada
- ✅ **Integração com Groq** (modelo Llama 3.1 8B)
- ✅ **Persistência de dados** em Oracle Database
- ✅ **Personalização de respostas** baseada no perfil do usuário (TB_GS_USUARIO)
- ✅ **Histórico de conversas** armazenado em TB_GS_CHAT_HISTORY
- ✅ **Documentação automática** via FastAPI/Swagger
- ✅ **Configuração via variáveis de ambiente**

## Requisitos

- Python 3.11+
- Oracle Database com estrutura criada (tabelas TB_GS_USUARIO e TB_GS_CHAT_HISTORY)
- Oracle Instant Client instalado
- Virtualenv (recomendado)
- Conta e chave de API da Groq (`https://console.groq.com/`)

## Configuração do Banco de Dados

**IMPORTANTE:** O aplicativo apenas se conecta ao banco Oracle existente. As tabelas devem estar previamente criadas.

1. **Execute o script SQL no seu banco Oracle:**
   ```sql
   -- Execute o script completo em:
   -- c:\Sistemas\gs-bd-remoteready\gs-bd-remoteready.sql
   ```

2. **Verifique se as tabelas existem:**
   ```sql
   SELECT table_name FROM user_tables 
   WHERE table_name IN ('TB_GS_USUARIO', 'TB_GS_CHAT_HISTORY');
   ```

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
   # Edite o arquivo .env com suas credenciais
   ```

## Variáveis de Ambiente

Configure no arquivo `.env`:

```env
# Configuração da API Groq
AI_API_KEY=sua_chave_groq_aqui
AI_API_URL=https://api.groq.com/openai/v1/chat/completions
AI_MODEL_NAME=llama-3.1-8b-instant
AI_TEMPERATURE=0.7
AI_MAX_TOKENS=512

# Configuração do Oracle Database
ORACLE_USER=seu_usuario
ORACLE_PASSWORD=sua_senha
ORACLE_DSN=localhost:1521/XEPDB1
```

## Execução da Aplicação

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

A API estará disponível em: `http://127.0.0.1:8000`

## Documentação da API

### Produção (Render)
- **Swagger UI:** [https://gs-iot-remoteready.onrender.com/docs](https://gs-iot-remoteready.onrender.com/docs)
- **ReDoc:** [https://gs-iot-remoteready.onrender.com/redoc](https://gs-iot-remoteready.onrender.com/redoc)

### Local
- **Swagger UI:** `http://127.0.0.1:8000/docs`
- **ReDoc:** `http://127.0.0.1:8000/redoc`

## Testando a API

### 1. Endpoint de Chat (POST /chat)

**IMPORTANTE:** O `user_id` deve existir na tabela `TB_GS_USUARIO` do Oracle.

#### Produção (Render)
```powershell
# Enviar mensagem para API em produção
Invoke-RestMethod -Uri "https://gs-iot-remoteready.onrender.com/chat" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"user_id": 1, "message": "Como melhorar meu foco em home office?"}'```

#### Local
```powershell
# Enviar mensagem para API local
Invoke-RestMethod -Uri "http://localhost:8000/chat" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"user_id": 1, "message": "Como melhorar meu foco em home office?"}'
```

**Resposta (200 OK):**
```json
{
  "answer": "Para melhorar seu foco em home office, recomendo..."
}
```

### 2. Endpoint de Histórico (GET /chat/history/{user_id})

#### Produção (Render)
```powershell
# Buscar histórico em produção
Invoke-RestMethod -Uri "https://gs-iot-remoteready.onrender.com/chat/history/1?limit=10" `
  -Method GET
```

#### Local
```powershell
# Buscar histórico local
Invoke-RestMethod -Uri "http://localhost:8000/chat/history/1?limit=10" `
  -Method GET
```

**Resposta (200 OK):**
```json
{
  "history": [
    {
      "id": 5,
      "prompt": "Como melhorar meu foco em home office?",
      "response": "Para melhorar seu foco...",
      "created_at": "2025-11-18T10:30:00"
    }
  ]
}
```

## Estrutura do Projeto

```
chatbot-iot/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI app e rotas
│   ├── models.py        # Modelos Pydantic (Request/Response)
│   ├── ai_client.py     # Cliente para API Groq + personalização
│   ├── oracle_db.py     # Conexão e operações Oracle
│   └── db.py            # [Legado] SQLite (não usado)
├── .env                 # Variáveis de ambiente (não commitar!)
├── .env.example         # Template de configuração
├── requirements.txt     # Dependências Python
├── README.md            # Este arquivo
└── README_ORACLE.md     # Documentação detalhada Oracle
```

## Tecnologias Utilizadas

- **FastAPI** - Framework web moderno para Python
- **Uvicorn** - Servidor ASGI para aplicações Python
- **HTTPx** - Cliente HTTP assíncrono
- **Python-dotenv** - Carregamento de variáveis de ambiente
- **Oracle Database** - Banco de dados enterprise
- **python-oracledb** - Driver oficial Oracle para Python
- **Groq API** - Serviço de LLM (Llama 3.1)

## Contexto da Global Solution

Este projeto demonstra a aplicação de tecnologias emergentes (IA/LLM) na solução de problemas reais do mercado de trabalho moderno, especificamente:

- **Problema:** Dificuldade de adaptação ao trabalho remoto/híbrido
- **Solução:** Chatbot especializado com orientações personalizadas baseadas no perfil do usuário
- **Impacto:** Melhoria na produtividade e qualidade de vida profissional

## Personalização por Perfil de Usuário

O chatbot adapta suas respostas baseado nos dados do usuário na `TB_GS_USUARIO`:

| Perfil | Experiência | Tipo de Resposta |
|--------|-------------|------------------|
| **JUNIOR** | 0-2 anos | Didática, explica conceitos básicos |
| **PLENO** | 3-5 anos | Direta ao ponto, intermediária |
| **SENIOR** | 5+ anos | Insights avançados e estratégicos |

### Dados utilizados para personalização:
- Nome do usuário
- Nível de experiência (JUNIOR/PLENO/SENIOR)
- Anos de trabalho
- Avaliação na plataforma

## Desenvolvimento e Testes

Para desenvolvimento com reload automático:
```powershell
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Para verificar o histórico de conversas no Oracle:
```sql
-- Ver últimas conversas
SELECT ID_CHAT, ID_USUARIO, 
       SUBSTR(DS_PROMPT, 1, 50) AS PROMPT,
       SUBSTR(DS_RESPONSE, 1, 50) AS RESPONSE,
       DT_CRIACAO
FROM TB_GS_CHAT_HISTORY
ORDER BY DT_CRIACAO DESC
FETCH FIRST 10 ROWS ONLY;

-- Verificar usuários cadastrados
SELECT ID_USUARIO, NM_USUARIO, TP_PERFIL, NR_EXPERIENCIA
FROM TB_GS_USUARIO
WHERE FL_ATIVO = 'Y';
```

## 🌐 Deploy em Produção

### Render.com

A aplicação está deployada no Render com as seguintes configurações:

**URLs de Produção:**
- Base URL: `https://gs-iot-remoteready.onrender.com`
- Documentação: `https://gs-iot-remoteready.onrender.com/docs`
- Endpoint Chat: `https://gs-iot-remoteready.onrender.com/chat`
- Histórico: `https://gs-iot-remoteready.onrender.com/chat/history/{user_id}`

**Configurações do Render:**
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **Environment:** Python 3
- **Plan:** Free Tier

**Variáveis de Ambiente (Render Dashboard):**
```
ORACLE_USER=seu_usuario
ORACLE_PASSWORD=sua_senha
ORACLE_DSN=seu_dsn_oracle
AI_API_KEY=sua_chave_groq
AI_API_URL=https://api.groq.com/openai/v1/chat/completions
AI_MODEL_NAME=llama-3.1-8b-instant
AI_TEMPERATURE=0.7
AI_MAX_TOKENS=512
```

**⚠️ Nota sobre Free Tier:**
- A primeira requisição pode demorar ~50s (cold start)
- Após 15 minutos de inatividade, o servidor hiberna
- Recomendado para testes e desenvolvimento

## Integração com Banco de Dados

### Tabelas Utilizadas:

**TB_GS_USUARIO** (leitura)
- Busca informações do usuário para personalização
- Campos: ID_USUARIO, NM_USUARIO, TP_PERFIL, NR_EXPERIENCIA, VL_AVALIACAO

**TB_GS_CHAT_HISTORY** (leitura/escrita)
- Armazena todas as conversas do chatbot
- Campos: ID_CHAT, ID_USUARIO, DS_PROMPT, DS_RESPONSE, DT_CRIACAO

### Fluxo de Dados:
1. Usuário envia mensagem com `user_id`
2. API busca perfil do usuário em `TB_GS_USUARIO`
3. Prompt é personalizado baseado no perfil
4. IA gera resposta contextualizada
5. Conversa é salva em `TB_GS_CHAT_HISTORY`
