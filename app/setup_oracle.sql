-- Script para criar a tabela de histórico de chat no Oracle
-- Execute este script no SQL Developer ou SQL*Plus conectado ao seu banco Oracle

-- Criar a tabela de histórico de chat
CREATE TABLE chat_history (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id NUMBER NOT NULL,
    user_message CLOB NOT NULL,
    bot_answer CLOB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Criar índice para melhor performance em consultas por user_id
CREATE INDEX idx_chat_history_user_id ON chat_history(user_id);

-- Criar índice para ordenação por data
CREATE INDEX idx_chat_history_created_at ON chat_history(created_at);

-- Comentários nas colunas para documentação
COMMENT ON TABLE chat_history IS 'Armazena o histórico de conversas do chatbot';
COMMENT ON COLUMN chat_history.id IS 'Identificador único da conversa';
COMMENT ON COLUMN chat_history.user_id IS 'ID do usuário que enviou a mensagem';
COMMENT ON COLUMN chat_history.user_message IS 'Mensagem enviada pelo usuário';
COMMENT ON COLUMN chat_history.bot_answer IS 'Resposta gerada pelo chatbot';
COMMENT ON COLUMN chat_history.created_at IS 'Data e hora da conversa';

-- Confirmar alterações
COMMIT;

-- Verificar a criação da tabela
SELECT table_name FROM user_tables WHERE table_name = 'CHAT_HISTORY';
