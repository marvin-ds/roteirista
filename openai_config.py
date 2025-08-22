import os
from openai import OpenAI

def get_openai_client():
    """
    Retorna um cliente OpenAI configurado com a chave da API.
    A chave deve ser definida na variável de ambiente OPENAI_API_KEY.
    """
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OPENAI_API_KEY não encontrada nas variáveis de ambiente")
    
    return OpenAI(api_key=api_key)

def validate_openai_key(api_key):
    """
    Valida se uma chave da API OpenAI é válida.
    
    Args:
        api_key (str): A chave da API para validar
        
    Returns:
        bool: True se a chave for válida, False caso contrário
    """
    try:
        client = OpenAI(api_key=api_key)
        # Tenta fazer uma requisição simples para validar a chave
        client.models.list()
        return True
    except Exception:
        return False