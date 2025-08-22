#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Finance-IA - Agente Roteirista - Serviço HTTP
API REST para processar ideias revisadas e gerar roteiros completos
Integrado com OpenAI GPT com segurança de chaves
"""

import json
import os
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional
from flask import Flask, request, jsonify
from roteirista_finance_ia import FinanceIARoteirista
from config import LISTAS_VALIDAS, REGRAS_LGPD_ETICA
# import logging - removido temporariamente para debug

# Configuração de logging removida temporariamente para debug
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
# )

app = Flask(__name__)

# Handler global removido temporariamente para debug

# Token de autenticação do agente (deve ser configurado via variável de ambiente)
AUTH_TOKEN = os.getenv('AUTH_TOKEN', 'finance-ia-token-default')

def mask_api_key(api_key: str) -> str:
    """
    Mascara a chave da API mostrando apenas os 4 últimos caracteres
    
    Args:
        api_key: Chave da API para mascarar
        
    Returns:
        Chave mascarada
    """
    if not api_key or len(api_key) < 4:
        return "****"
    return "****" + api_key[-4:]

def get_openai_key_from_request() -> tuple[Optional[str], Optional[Dict[str, Any]]]:
    """
    Extrai a chave da OpenAI da requisição seguindo a ordem de prioridade:
    1. Header X-OPENAI-API-KEY (preferencial)
    2. Corpo JSON, campo openai_api_key (opcional)
    3. Variável de ambiente OPENAI_API_KEY (fallback)
    
    Returns:
        Tupla (chave_openai, erro_dict)
        Se erro_dict não for None, deve retornar erro 401
    """
    
    # 1. Verificar header X-OPENAI-API-KEY (preferencial)
    openai_key = request.headers.get('X-OPENAI-API-KEY')
    if openai_key:
        # app.logger.info(f"Chave OpenAI obtida do header: {mask_api_key(openai_key)}")
        return openai_key, None
    
    # 2. Verificar corpo JSON, campo openai_api_key (opcional)
    try:
        if request.is_json and request.json:
            body_key = request.json.get('openai_api_key')
            if body_key:
                # app.logger.info(f"Chave OpenAI obtida do body: {mask_api_key(body_key)}")
                return body_key, None
    except Exception as e:
        # app.logger.warning(f"Erro ao ler chave do body JSON: {str(e)}")
        pass
    
    # 3. Verificar variável de ambiente OPENAI_API_KEY (fallback)
    env_key = os.getenv('OPENAI_API_KEY')
    if env_key:
        # app.logger.info(f"Chave OpenAI obtida da variável de ambiente: {mask_api_key(env_key)}")
        return env_key, None
    
    # Nenhuma fonte forneceu a chave
    # app.logger.warning("Chave OpenAI não encontrada em nenhuma fonte")
    return None, {
        "error": "missing_openai_key",
        "hint": "Envie em X-OPENAI-API-KEY ou defina OPENAI_API_KEY"
    }

def verify_auth_token() -> Optional[Dict[str, Any]]:
    """
    Verifica o token de autenticação do agente
    
    Returns:
        Dicionário de erro se token inválido, None se válido
    """
    auth_header = request.headers.get('Authorization', '')
    
    if not auth_header.startswith('Bearer '):
        return {
            "error": "missing_auth_token",
            "hint": "Envie Authorization: Bearer <AUTH_TOKEN>"
        }
    
    token = auth_header[7:]  # Remove 'Bearer '
    
    if token != AUTH_TOKEN:
        return {
            "error": "invalid_auth_token",
            "hint": "Token de autenticação inválido"
        }
    
    return None

def sanitize_error_message(error_msg: str) -> str:
    """
    Sanitiza mensagens de erro para evitar vazamento de informações sensíveis
    
    Args:
        error_msg: Mensagem de erro original
        
    Returns:
        Mensagem sanitizada
    """
    # Remove possíveis chaves de API ou tokens das mensagens
    sensitive_patterns = ['sk-', 'Bearer ', 'api_key', 'token']
    
    sanitized = error_msg
    for pattern in sensitive_patterns:
        if pattern in sanitized:
            sanitized = sanitized.replace(pattern, '[REDACTED]')
    
    return sanitized

@app.route('/healthz', methods=['GET'])
def health_check():
    """
    Endpoint de health check que não acessa a OpenAI
    
    Returns:
        Status 200 com informações básicas do sistema
    """
    return jsonify({
        "status": "healthy",
        "service": "finance-ia-roteirista",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }), 200

@app.route('/test-debug', methods=['POST'])
def test_debug():
    """
    Endpoint de teste para debug - versão ultra simples
    """
    return "OK", 200

@app.route('/test-debug-full', methods=['POST'])
def test_debug_full():
    """
    Endpoint de teste para debug - versão completa
    """
    try:
        print("🧪 ENDPOINT DE TESTE COMPLETO CHAMADO!")
        print(f"📋 Headers: {dict(request.headers)}")
        print(f"📦 Body: {request.get_data(as_text=True)}")
        return jsonify({"message": "Debug test successful"}), 200
    except Exception as e:
        print(f"🔥 ERRO NO ENDPOINT DE TESTE: {str(e)}")
        import traceback
        print(f"🔍 STACK TRACE DO TESTE:")
        print(traceback.format_exc())
        return jsonify({
            "error": "test_debug_error",
            "message": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@app.route('/processar', methods=['POST'])
def processar_ideia():
    """
    Endpoint principal para processar ideias revisadas
    
    Returns:
        JSON com roteiro gerado ou erro
    """
    trace_id = str(uuid.uuid4())
    print(f"🚀 REQUISIÇÃO RECEBIDA [{trace_id}]: /processar")
    print(f"📋 Headers: {dict(request.headers)}")
    print(f"📦 Body: {request.get_data(as_text=True)[:500]}...")
    
    try:
        # Verificar token de autenticação
        auth_error = verify_auth_token()
        if auth_error:
            # app.logger.warning(f"[{trace_id}] Falha na autenticação: {auth_error['error']}")
            return jsonify(auth_error), 401
        
        # Obter chave da OpenAI
        openai_key, key_error = get_openai_key_from_request()
        if key_error:
            # app.logger.warning(f"[{trace_id}] Chave OpenAI ausente")
            return jsonify(key_error), 401
        
        # Verificar se há dados JSON na requisição
        if not request.is_json:
            return jsonify({
                "error": "invalid_content_type",
                "hint": "Content-Type deve ser application/json"
            }), 400
        
        # Obter dados da requisição (removendo chave OpenAI para log)
        request_data = request.json.copy() if request.json else {}
        if 'openai_api_key' in request_data:
            del request_data['openai_api_key']  # Remove para não logar
        
        # app.logger.info(f"[{trace_id}] Processando ideia: {json.dumps(request_data, ensure_ascii=False)[:200]}...")
        
        # Criar instância do roteirista (sem armazenar a chave)
        roteirista = FinanceIARoteirista()
        
        # Processar a ideia passando a chave como parâmetro
        resultado = roteirista.processar_ideia_revisada(request.json, openai_api_key=openai_key)
        
        # app.logger.info(f"[{trace_id}] Processamento concluído com sucesso")
        
        return jsonify({
            "sucesso": True,
            "dados": resultado,
            "versao_sistema": "1.0.0",
            "processado_em": datetime.now().isoformat(),
            "trace_id": trace_id
        }), 200
        
    except Exception as e:
        error_msg = str(e)  # Temporariamente sem sanitização para debug
        print(f"🔥 ERRO CAPTURADO [{trace_id}]: {error_msg}")
        import traceback
        stack_trace = traceback.format_exc()
        print(f"🔍 STACK TRACE [{trace_id}]:")
        print(stack_trace)
        # app.logger.error(f"[{trace_id}] Erro interno: {error_msg}")
        # app.logger.error(f"[{trace_id}] Stack trace: {stack_trace}")
        
        # Verificar se é erro da OpenAI
        if 'openai' in error_msg.lower() or 'api' in error_msg.lower():
            return jsonify({
                "error": "openai_client_error",
                "detail": error_msg,
                "trace_id": trace_id
            }), 502
        
        return jsonify({
            "error": "internal_error",
            "trace_id": trace_id
        }), 500

@app.route('/validar', methods=['POST'])
def validar_entrada():
    """
    Endpoint para validar entrada sem processar
    
    Returns:
        JSON com resultado da validação
    """
    trace_id = str(uuid.uuid4())
    
    try:
        # Verificar token de autenticação
        auth_error = verify_auth_token()
        if auth_error:
            return jsonify(auth_error), 401
        
        # Verificar se há dados JSON na requisição
        if not request.is_json:
            return jsonify({
                "error": "invalid_content_type",
                "hint": "Content-Type deve ser application/json"
            }), 400
        
        # Validar entrada (não precisa de chave OpenAI)
        roteirista = FinanceIARoteirista()
        
        try:
            roteirista._validar_ideia_revisada(request.json)
            return jsonify({
                "valido": True,
                "trace_id": trace_id
            }), 200
        except ValueError as e:
            return jsonify({
                "valido": False,
                "erro": str(e),
                "trace_id": trace_id
            }), 400
            
    except Exception as e:
        error_msg = sanitize_error_message(str(e))
        # app.logger.error(f"[{trace_id}] Erro na validação: {error_msg}")
        
        return jsonify({
            "error": "internal_error",
            "trace_id": trace_id
        }), 500

@app.route('/listas', methods=['GET'])
def obter_listas():
    """
    Endpoint para obter listas de valores válidos
    
    Returns:
        JSON com listas válidas
    """
    try:
        # Verificar token de autenticação
        auth_error = verify_auth_token()
        if auth_error:
            return jsonify(auth_error), 401
        
        return jsonify({
            "listas_validas": LISTAS_VALIDAS,
            "regras_lgpd": REGRAS_LGPD_ETICA
        }), 200
        
    except Exception as e:
        error_msg = sanitize_error_message(str(e))
        # app.logger.error(f"Erro ao obter listas: {error_msg}")
        
        return jsonify({
            "error": "internal_error"
        }), 500

@app.route('/template', methods=['GET'])
def obter_template():
    """
    Endpoint para obter template de entrada
    
    Returns:
        JSON com template de entrada
    """
    try:
        # Verificar token de autenticação
        auth_error = verify_auth_token()
        if auth_error:
            return jsonify(auth_error), 401
        
        template = {
            "data_da_semana": datetime.now().strftime("%Y-%m-%d"),
            "tema": "Como organizar o orçamento familiar sem brigas",
            "persona": "Casal",
            "pilar": "Orçamento",
            "formato": "Reel/Short",
            "canal": "Instagram",
            "cta": "Comunidade Telegram",
            "kpi_principal": "CTR",
            "status": "Ideia",
            "roteirizado_em": "",
            "publicado_em": "",
            "lgpd_ok": "Sim",
            "prioridade": "Alta",
            "links_assets": "",
            "observacoes": "dor: brigas por dinheiro | desejo: harmonia financeira"
        }
        
        return jsonify({
            "template": template,
            "listas_validas": LISTAS_VALIDAS
        }), 200
        
    except Exception as e:
        error_msg = sanitize_error_message(str(e))
        # app.logger.error(f"Erro ao obter template: {error_msg}")
        
        return jsonify({
            "error": "internal_error"
        }), 500

if __name__ == '__main__':
    
    # Verificar configurações
    if not AUTH_TOKEN or AUTH_TOKEN == 'finance-ia-token-default':
        print("⚠️  AVISO: AUTH_TOKEN não configurado ou usando valor padrão")
        print("   Configure a variável de ambiente AUTH_TOKEN")
    
    print("🚀 Finance-IA Roteirista API iniciando...")
    print(f"   Porta: {os.getenv('PORT', 5000)}")
    print(f"   Debug: {os.getenv('FLASK_DEBUG', 'False')}")
    
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5000)),
        debug=os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    )