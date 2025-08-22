#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Finance-IA - Agente Roteirista - Interface Principal (API)
Sistema para processar ideias revisadas e gerar roteiros completos
Integrado com OpenAI GPT para geração inteligente de conteúdo
"""

import json
import sys
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
from roteirista_finance_ia import FinanceIARoteirista, processar_roteiro
from config import LISTAS_VALIDAS, REGRAS_LGPD_ETICA

class FinanceIAAPI:
    """
    Interface principal do sistema Finance-IA Roteirista
    Fornece métodos para integração com sistemas externos
    Integrado com OpenAI GPT para geração inteligente de conteúdo
    """
    
    def __init__(self, openai_api_key: str = None):
        # Usar chave fornecida ou variável de ambiente
        api_key = openai_api_key or os.getenv('OPENAI_API_KEY')
        self.roteirista = FinanceIARoteirista(openai_api_key=api_key)
        self.versao = "1.0.0"
    
    def processar_ideia_json(self, ideia_json: str) -> Dict[str, Any]:
        """
        Processa uma ideia revisada em formato JSON
        
        Args:
            ideia_json: String JSON com a ideia revisada
            
        Returns:
            Dicionário com o roteiro gerado ou erro
        """
        
        try:
            # Parse do JSON de entrada
            ideia = json.loads(ideia_json)
            
            # Validar entrada
            validacao = self.validar_entrada(ideia)
            if not validacao["valido"]:
                return {
                    "sucesso": False,
                    "erro": f"Entrada inválida: {validacao['erro']}",
                    "codigo_erro": "ENTRADA_INVALIDA"
                }
            
            # Processar roteiro
            resultado = self.roteirista.processar_ideia_revisada(ideia)
            
            return {
                "sucesso": True,
                "dados": resultado,
                "versao_sistema": self.versao,
                "processado_em": datetime.now().isoformat()
            }
            
        except json.JSONDecodeError as e:
            return {
                "sucesso": False,
                "erro": f"JSON inválido: {str(e)}",
                "codigo_erro": "JSON_INVALIDO"
            }
        except Exception as e:
            return {
                "sucesso": False,
                "erro": f"Erro interno: {str(e)}",
                "codigo_erro": "ERRO_INTERNO"
            }
    
    def validar_entrada(self, ideia: Dict[str, Any]) -> Dict[str, Any]:
        """
        Valida se a entrada está no formato correto
        
        Args:
            ideia: Dicionário com a ideia revisada
            
        Returns:
            Dicionário com resultado da validação
        """
        
        # Campos obrigatórios
        campos_obrigatorios = [
            "data_da_semana", "tema", "persona", "pilar", "formato",
            "canal", "cta", "kpi_principal", "status", "prioridade"
        ]
        
        # Verificar campos obrigatórios
        for campo in campos_obrigatorios:
            if campo not in ideia:
                return {
                    "valido": False,
                    "erro": f"Campo obrigatório ausente: {campo}"
                }
        
        # Validar valores contra listas válidas
        validacoes = [
            ("persona", "personas"),
            ("pilar", "pilares"),
            ("formato", "formatos"),
            ("canal", "canais"),
            ("cta", "ctas"),
            ("kpi_principal", "kpis"),
            ("prioridade", "prioridade")
        ]
        
        for campo, lista_valida in validacoes:
            valor = ideia.get(campo)
            if valor not in LISTAS_VALIDAS[lista_valida]:
                return {
                    "valido": False,
                    "erro": f"Valor inválido para {campo}: {valor}. Valores válidos: {LISTAS_VALIDAS[lista_valida]}"
                }
        
        # Validar formato da data
        try:
            datetime.strptime(ideia["data_da_semana"], "%Y-%m-%d")
        except ValueError:
            return {
                "valido": False,
                "erro": "Formato de data inválido. Use YYYY-MM-DD"
            }
        
        # Validar LGPD
        lgpd_check = self.verificar_lgpd(ideia)
        if not lgpd_check["conforme"]:
            return {
                "valido": False,
                "erro": f"Violação LGPD: {lgpd_check['violacao']}"
            }
        
        return {"valido": True}
    
    def verificar_lgpd(self, ideia: Dict[str, Any]) -> Dict[str, Any]:
        """
        Verifica conformidade com LGPD e regras éticas
        
        Args:
            ideia: Dicionário com a ideia revisada
            
        Returns:
            Dicionário com resultado da verificação
        """
        
        tema = ideia.get("tema", "").lower()
        observacoes = ideia.get("observacoes", "").lower()
        
        # Verificar promessas proibidas
        for promessa in REGRAS_LGPD_ETICA["promessas_proibidas"]:
            if promessa in tema or promessa in observacoes:
                return {
                    "conforme": False,
                    "violacao": f"Promessa irreal detectada: '{promessa}'"
                }
        
        # Verificar dados pessoais (básico)
        termos_suspeitos = ["cpf", "telefone", "nome completo", "conta bancária"]
        for termo in termos_suspeitos:
            if termo in tema or termo in observacoes:
                return {
                    "conforme": False,
                    "violacao": f"Possível referência a dados pessoais: '{termo}'"
                }
        
        return {"conforme": True}
    
    def obter_listas_validas(self) -> Dict[str, Any]:
        """
        Retorna todas as listas de valores válidos
        
        Returns:
            Dicionário com listas válidas
        """
        
        return {
            "listas_validas": LISTAS_VALIDAS,
            "versao_sistema": self.versao
        }
    
    def obter_template_entrada(self) -> Dict[str, Any]:
        """
        Retorna template de entrada para facilitar integração
        
        Returns:
            Dicionário com template de entrada
        """
        
        return {
            "template": {
                "data_da_semana": "YYYY-MM-DD",
                "tema": "string curta (dor/desejo explícito)",
                "persona": "valor de listas_validas.personas",
                "pilar": "valor de listas_validas.pilares",
                "formato": "valor de listas_validas.formatos",
                "canal": "valor de listas_validas.canais",
                "cta": "valor de listas_validas.ctas",
                "kpi_principal": "valor de listas_validas.kpis",
                "status": "Ideia",
                "roteirizado_em": "",
                "publicado_em": "",
                "lgpd_ok": "Sim",
                "prioridade": "valor de listas_validas.prioridade",
                "links_assets": "",
                "observacoes": "ex.: dor: ... | desejo: ..."
            },
            "listas_validas": LISTAS_VALIDAS
        }
    
    def processar_lote(self, ideias_json: str) -> Dict[str, Any]:
        """
        Processa múltiplas ideias em lote
        
        Args:
            ideias_json: String JSON com array de ideias
            
        Returns:
            Dicionário com resultados do lote
        """
        
        try:
            ideias = json.loads(ideias_json)
            
            if not isinstance(ideias, list):
                return {
                    "sucesso": False,
                    "erro": "Entrada deve ser um array de ideias",
                    "codigo_erro": "FORMATO_LOTE_INVALIDO"
                }
            
            resultados = []
            sucessos = 0
            erros = 0
            
            for i, ideia in enumerate(ideias):
                try:
                    resultado = self.roteirista.processar_ideia_revisada(ideia)
                    resultados.append({
                        "indice": i,
                        "sucesso": True,
                        "dados": resultado
                    })
                    sucessos += 1
                except Exception as e:
                    resultados.append({
                        "indice": i,
                        "sucesso": False,
                        "erro": str(e)
                    })
                    erros += 1
            
            return {
                "sucesso": True,
                "total_processado": len(ideias),
                "sucessos": sucessos,
                "erros": erros,
                "resultados": resultados,
                "processado_em": datetime.now().isoformat()
            }
            
        except json.JSONDecodeError as e:
            return {
                "sucesso": False,
                "erro": f"JSON inválido: {str(e)}",
                "codigo_erro": "JSON_INVALIDO"
            }
        except Exception as e:
            return {
                "sucesso": False,
                "erro": f"Erro interno: {str(e)}",
                "codigo_erro": "ERRO_INTERNO"
            }

def main():
    """
    Interface de linha de comando para o Finance-IA Roteirista
    """
    if len(sys.argv) < 2:
        print("Uso: python main.py <comando> [arquivo] [--openai-key=<chave>]")
        print("Comandos disponíveis:")
        print("  exemplo - Gerar exemplo de roteiro")
        print("  processar <arquivo.json> - Processar arquivo de ideia")
        print("  validar <arquivo.json> - Validar arquivo de entrada")
        print("  template - Mostrar template de entrada")
        print("  listas - Mostrar listas de valores válidos")
        print("")
        print("Opções:")
        print("  --openai-key=<chave> - Chave da API OpenAI (ou use OPENAI_API_KEY)")
        return
    
    comando = sys.argv[1].lower()
    
    # Extrair chave da OpenAI dos argumentos
    openai_key = None
    for arg in sys.argv:
        if arg.startswith('--openai-key='):
            openai_key = arg.split('=', 1)[1]
            break
    
    # Se não fornecida via argumento, tentar variável de ambiente
    if not openai_key:
        openai_key = os.getenv('OPENAI_API_KEY')
    
    # Definir a chave como variável de ambiente se fornecida
    if openai_key:
        os.environ['OPENAI_API_KEY'] = openai_key
        print(f"✅ Usando OpenAI API (chave: ...{openai_key[-8:] if len(openai_key) > 8 else 'configurada'})")
    else:
        print("⚠️  OpenAI API não configurada - sistema funcionará em modo básico")
    
    api = FinanceIAAPI(openai_api_key=openai_key)
    
    if comando == "processar":
        if len(sys.argv) < 3:
            print("Erro: Especifique o arquivo JSON")
            return
        
        try:
            with open(sys.argv[2], 'r', encoding='utf-8') as f:
                ideia_json = f.read()
            
            resultado = api.processar_ideia_json(ideia_json)
            print(json.dumps(resultado, ensure_ascii=False, indent=2))
            
        except FileNotFoundError:
            print(f"Erro: Arquivo {sys.argv[2]} não encontrado")
        except Exception as e:
            print(f"Erro: {str(e)}")
    
    elif comando == "validar":
        if len(sys.argv) < 3:
            print("Erro: Especifique o arquivo JSON")
            return
        
        try:
            with open(sys.argv[2], 'r', encoding='utf-8') as f:
                ideia_json = f.read()
            
            ideia = json.loads(ideia_json)
            validacao = api.validar_entrada(ideia)
            
            if validacao["valido"]:
                print("✅ Entrada válida!")
            else:
                print(f"❌ Entrada inválida: {validacao['erro']}")
            
        except FileNotFoundError:
            print(f"Erro: Arquivo {sys.argv[2]} não encontrado")
        except Exception as e:
            print(f"Erro: {str(e)}")
    
    elif comando == "template":
        template = api.obter_template_entrada()
        print(json.dumps(template, ensure_ascii=False, indent=2))
    
    elif comando == "listas":
        listas = api.obter_listas_validas()
        print(json.dumps(listas, ensure_ascii=False, indent=2))
    
    elif comando == "exemplo":
        exemplo_ideia = {
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
        
        resultado = api.processar_ideia_json(json.dumps(exemplo_ideia))
        print(json.dumps(resultado, ensure_ascii=False, indent=2))
    
    else:
        print(f"Comando desconhecido: {comando}")

if __name__ == "__main__":
    main()