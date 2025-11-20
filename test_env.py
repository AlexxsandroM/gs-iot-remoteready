#!/usr/bin/env python3
"""Script de teste para verificar se .env está sendo carregado."""

import os
from dotenv import load_dotenv

print("Antes do load_dotenv:")
print(f"AI_API_KEY: {os.getenv('AI_API_KEY')}")
print(f"AI_API_URL: {os.getenv('AI_API_URL')}")

load_dotenv()

print("\nDepois do load_dotenv:")
print(f"AI_API_KEY: {os.getenv('AI_API_KEY')}")
print(f"AI_API_URL: {os.getenv('AI_API_URL')}")
print(f"AI_MODEL_NAME: {os.getenv('AI_MODEL_NAME')}")

# Verificar se arquivo .env existe
if os.path.exists('.env'):
    print("\nArquivo .env encontrado!")
    with open('.env', 'r') as f:
        print("Conteúdo do .env:")
        print(f.read())
else:
    print("\nARQUIVO .env NÃO ENCONTRADO!")