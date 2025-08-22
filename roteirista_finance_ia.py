#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Finance-IA - Agente Roteirista
Sistema para gerar roteiros prontos para produção de conteúdo de educação financeira
Integrado com OpenAI GPT para geração inteligente de conteúdo
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any

try:
    import openai
except ImportError:
    print("Aviso: Biblioteca openai não encontrada. Instale com: pip install openai")
    openai = None

class FinanceIARoteirista:
    """
    Classe principal do Agente Roteirista do Finance-IA
    Processa ideias revisadas e gera roteiros completos para produção
    Integrada com OpenAI GPT para geração inteligente de conteúdo
    """
    
    def __init__(self, openai_api_key: str = None):
        self.listas_validas = {
            "personas": ["Jovem Adulto", "Casal", "Família", "Empreendedor", "Aposentado"],
            "pilares": ["Orçamento", "Investimentos", "Dívidas", "Renda Extra", "Planejamento"],
            "formatos": ["Reel/Short", "YouTube Longo", "Carrossel", "Post Telegram", "Stories/Status"],
            "canais": ["Instagram", "TikTok", "YouTube", "Telegram", "WhatsApp"],
            "ctas": ["Comunidade Telegram", "WhatsApp Diagnóstico", "Download Planilha", "Curso Gratuito"],
            "kpis": ["CTR", "Salvamentos", "Retenção", "Engajamento", "Conversão"],
            "prioridade": ["Alta", "Média", "Baixa"]
        }
        
        self.regras_narracao = {
            "idioma": "português do Brasil",
            "publico": "leigos",
            "estilo": "frases curtas, verbos de ação, sem jargões",
            "termos_tecnicos": "explicar em 1 linha quando necessário"
        }
        
        self.regras_visual = {
            "tipo": "categorias genéricas",
            "exemplos": ["ícone de orçamento", "gráfico simples", "mãos ajustando planilha"],
            "proibido": "fotos que identifiquem pessoas/dados pessoais"
        }
        
        self.regras_musica = {
            "especificar": "mood e bpm",
            "proibido": "músicas comerciais específicas",
            "preferencia": "biblioteca sem direitos/livre de royalties",
            "sfx": "sutil (whoosh, click)"
        }
        
        self.ajustes_kpi = {
            "CTR": "CTA no meio e final, reforçar benefício claro",
            "Salvamentos": "checklist em 3 passos e bullets copiáveis",
            "Retenção": "open loop no início, variação visual a cada 3-5s"
        }
        
        self.regras_lgpd = {
            "proibido": ["nomes completos", "telefones", "CPFs", "valores bancários", "prints com PII"],
            "promessas_irreais": ["garantido", "fique rico", "100% certo"],
            "tom": "acolhedor e não-julgador",
            "foco": "1 ação prática hoje"
        }
        
        # Verificar disponibilidade da OpenAI (sem armazenar a chave)
        # A chave será passada como parâmetro nos métodos que precisam
        self._openai_key_for_session = openai_api_key or os.getenv('OPENAI_API_KEY')
        if not self._openai_key_for_session:
            print("Aviso: OPENAI_API_KEY não configurada. Sistema funcionará em modo básico.")
        if not openai:
            print("Aviso: Biblioteca openai não instalada. Sistema funcionará em modo básico.")
    
    def processar_ideia_revisada(self, ideia_revisada: Dict[str, Any], openai_api_key: str = None) -> Dict[str, Any]:
        """
        Processa uma ideia revisada e gera o roteiro completo
        
        Args:
            ideia_revisada: Dicionário com os campos da ideia revisada
            openai_api_key: Chave da API OpenAI (opcional)
            
        Returns:
            Dicionário com o roteiro completo e atualizações da planilha
        """
        
        # Validar entrada
        self._validar_ideia_revisada(ideia_revisada)
        
        # Gerar roteiro baseado no formato
        formato = ideia_revisada["formato"]
        
        if formato == "Reel/Short":
            roteiro = self._gerar_roteiro_reel_short(ideia_revisada, openai_api_key=openai_api_key)
        elif formato == "YouTube Longo":
            roteiro = self._gerar_roteiro_youtube_longo(ideia_revisada, openai_api_key=openai_api_key)
        elif formato == "Carrossel":
            roteiro = self._gerar_roteiro_carrossel(ideia_revisada, openai_api_key=openai_api_key)
        elif formato == "Post Telegram":
            roteiro = self._gerar_roteiro_post_telegram(ideia_revisada)
        elif formato == "Stories/Status":
            roteiro = self._gerar_roteiro_stories_status(ideia_revisada)
        else:
            raise ValueError(f"Formato não suportado: {formato}")
        
        # Aplicar ajustes baseados no KPI
        roteiro = self._aplicar_ajustes_kpi(roteiro, ideia_revisada["kpi_principal"])
        
        # Preparar resposta final
        resposta = {
            "roteiro": roteiro,
            "atualizacoes_planilha": {
                "status": "Em roteiro",
                "roteirizado_em": datetime.now().strftime("%Y-%m-%d"),
                "links_assets": ""
            }
        }
        
        return resposta
    
    def _validar_ideia_revisada(self, ideia: Dict[str, Any]) -> None:
        """
        Valida se a ideia revisada contém todos os campos obrigatórios
        """
        campos_obrigatorios = [
            "data_da_semana", "tema", "persona", "pilar", "formato",
            "canal", "cta", "kpi_principal", "status", "prioridade"
        ]
        
        for campo in campos_obrigatorios:
            if campo not in ideia:
                raise ValueError(f"Campo obrigatório ausente: {campo}")
    
    def _gerar_roteiro_reel_short(self, ideia: Dict[str, Any], openai_api_key: str = None) -> Dict[str, Any]:
        """
        Gera roteiro para Reel/Short (Instagram, TikTok, YouTube Shorts)
        Formato: 9:16, 20-45s
        """
        
        tema_refinado = self._refinar_tema(ideia["tema"])
        cta_final = self._gerar_cta_final(ideia["cta"], openai_api_key=openai_api_key)
        
        segmentos = [
            {
                "nome": "Hook",
                "inicio_s": 0,
                "fim_s": 2,
                "narracao": f"Você sabia que {tema_refinado.lower()}? Vou te mostrar como resolver isso em 3 passos simples.",
                "texto_na_tela": "3 PASSOS SIMPLES",
                "visual_sugestoes": ["tipografia cinética", "ícone relacionado à dor financeira"],
                "efeitos_corte": ["corte seco", "zoom leve"],
                "musica_sugestao": {"mood": "otimista", "bpm": "100-110", "tipo": "biblioteca sem direitos"},
                "sfx_sugestao": ["whoosh suave"]
            },
            {
                "nome": "Passo 1",
                "inicio_s": 2,
                "fim_s": 8,
                "narracao": "Primeiro passo: anote todos os seus gastos por uma semana. Use o celular, um caderno, qualquer coisa.",
                "texto_na_tela": "PASSO 1: ANOTE TUDO",
                "visual_sugestoes": ["ícone de anotação", "mãos escrevendo", "app de notas"],
                "efeitos_corte": ["transição suave"],
                "musica_sugestao": {"mood": "focado", "bpm": "95-105", "tipo": "biblioteca sem direitos"},
                "sfx_sugestao": ["click suave"]
            },
            {
                "nome": "Passo 2",
                "inicio_s": 8,
                "fim_s": 15,
                "narracao": "Segundo passo: separe os gastos em categorias. Comida, transporte, lazer. Assim você vê onde o dinheiro vai.",
                "texto_na_tela": "PASSO 2: CATEGORIZE",
                "visual_sugestoes": ["gráfico simples por categorias", "ícones de categorias"],
                "efeitos_corte": ["slide lateral"],
                "musica_sugestao": {"mood": "organizativo", "bpm": "100-110", "tipo": "biblioteca sem direitos"},
                "sfx_sugestao": ["whoosh"]
            },
            {
                "nome": "Passo 3",
                "inicio_s": 15,
                "fim_s": 22,
                "narracao": "Terceiro passo: defina um limite para cada categoria. Comece com 10% menos do que você gastou na semana.",
                "texto_na_tela": "PASSO 3: DEFINA LIMITES",
                "visual_sugestoes": ["calculadora simples", "gráfico com limites"],
                "efeitos_corte": ["zoom in"],
                "musica_sugestao": {"mood": "determinado", "bpm": "105-115", "tipo": "biblioteca sem direitos"},
                "sfx_sugestao": ["ding suave"]
            },
            {
                "nome": "Prova visual",
                "inicio_s": 22,
                "fim_s": 28,
                "narracao": "Fazendo isso, você pode economizar até 200 reais por mês. É dinheiro que estava escapando sem você perceber.",
                "texto_na_tela": "ECONOMIA: R$ 200/MÊS",
                "visual_sugestoes": ["números destacados", "ícone de economia", "mini planilha"],
                "efeitos_corte": ["destaque numérico"],
                "musica_sugestao": {"mood": "conquista", "bpm": "110-120", "tipo": "biblioteca sem direitos"},
                "sfx_sugestao": ["chime de sucesso"]
            },
            {
                "nome": "CTA final",
                "inicio_s": 28,
                "fim_s": 32,
                "narracao": cta_final,
                "texto_na_tela": "LINK NA BIO",
                "visual_sugestoes": ["call to action visual", "seta apontando"],
                "efeitos_corte": ["fade out"],
                "musica_sugestao": {"mood": "convidativo", "bpm": "100-110", "tipo": "biblioteca sem direitos"},
                "sfx_sugestao": ["whoosh final"]
            }
        ]
        
        return {
            "formato": ideia["formato"],
            "canal": ideia["canal"],
            "persona": ideia["persona"],
            "pilar": ideia["pilar"],
            "tema": tema_refinado,
            "kpi_principal": ideia["kpi_principal"],
            "cta_final": cta_final,
            "diretrizes_execucao": {
                "aspect_ratio": "9:16",
                "duracao_alvo_segundos": 32,
                "tom_de_voz": ["didático", "empático", "prático", "confiável", "moderno"],
                "observacoes": self._extrair_observacoes(ideia.get("observacoes", ""))
            },
            "segmentos": segmentos,
            "meta_publicacao": {
                "legenda": f"💰 {tema_refinado}\n\nSiga estes 3 passos simples e comece a economizar hoje mesmo!\n\n{cta_final}\n\n❓ Qual é a sua maior dificuldade com o orçamento?",
                "hashtags": ["#educacaofinanceira", "#orcamento", "#economia", "#dinheiro", "#financas"],
                "thumb_titulo": "3 Passos para Economizar"
            },
            "assets_sugeridos": [
                "Ícones de categorias financeiras (comida, transporte, lazer)",
                "Gráficos simples de orçamento",
                "Tipografia cinética para números",
                "Paleta de cores: azul confiança + verde economia"
            ]
        }
    
    def _gerar_roteiro_youtube_longo(self, ideia: Dict[str, Any], openai_api_key: str = None) -> Dict[str, Any]:
        """
        Gera roteiro para YouTube Longo
        Formato: 16:9, 8-12 min
        """
        
        tema_refinado = self._refinar_tema(ideia["tema"])
        cta_final = self._gerar_cta_final(ideia["cta"], openai_api_key=openai_api_key)
        
        segmentos = [
            {
                "nome": "Hook",
                "inicio_s": 0,
                "fim_s": 30,
                "narracao": f"Se você está lutando com {tema_refinado.lower()}, este vídeo vai mudar sua vida financeira. Vou te mostrar um método que já ajudou milhares de pessoas.",
                "texto_na_tela": "MÉTODO COMPROVADO",
                "visual_sugestoes": ["apresentação pessoal", "preview dos resultados"],
                "efeitos_corte": ["cortes dinâmicos"],
                "musica_sugestao": {"mood": "inspirador", "bpm": "90-100", "tipo": "biblioteca sem direitos"},
                "sfx_sugestao": ["intro musical"]
            },
            {
                "nome": "Contexto",
                "inicio_s": 30,
                "fim_s": 120,
                "narracao": "Antes de mais nada, quero que você saiba que não está sozinho nessa. A maioria das pessoas nunca aprendeu a lidar com dinheiro na escola.",
                "texto_na_tela": "VOCÊ NÃO ESTÁ SOZINHO",
                "visual_sugestoes": ["estatísticas brasileiras", "gráficos de endividamento"],
                "efeitos_corte": ["transições suaves"],
                "musica_sugestao": {"mood": "empático", "bpm": "80-90", "tipo": "biblioteca sem direitos"},
                "sfx_sugestao": ["transições sutis"]
            }
            # Adicionar mais segmentos conforme necessário
        ]
        
        return {
            "formato": ideia["formato"],
            "canal": ideia["canal"],
            "persona": ideia["persona"],
            "pilar": ideia["pilar"],
            "tema": tema_refinado,
            "kpi_principal": ideia["kpi_principal"],
            "cta_final": cta_final,
            "diretrizes_execucao": {
                "aspect_ratio": "16:9",
                "duracao_alvo_segundos": 600,
                "tom_de_voz": ["didático", "empático", "confiável", "inspirador"],
                "observacoes": self._extrair_observacoes(ideia.get("observacoes", ""))
            },
            "segmentos": segmentos,
            "capitulos_timestamps": [
                "00:00 - Introdução",
                "00:30 - Por que isso acontece",
                "02:00 - Método passo a passo",
                "07:00 - Exemplo prático",
                "09:00 - Erros comuns",
                "10:30 - Próximos passos"
            ],
            "meta_publicacao": {
                "legenda": f"🎯 {tema_refinado}\n\nNeste vídeo completo, você vai aprender:\n• Como organizar suas finanças\n• Método passo a passo\n• Exemplo prático\n• Erros que você deve evitar\n\n{cta_final}\n\n💬 Deixe seu comentário: qual sua maior dificuldade financeira?",
                "hashtags": ["#educacaofinanceira", "#orcamento", "#planejamentofinanceiro"],
                "thumb_titulo": "Como Organizar Suas Finanças"
            },
            "assets_sugeridos": [
                "Slides explicativos simples",
                "Planilha de exemplo (sem dados reais)",
                "Gráficos de progresso",
                "B-roll de situações cotidianas"
            ]
        }
    
    def _gerar_roteiro_carrossel(self, ideia: Dict[str, Any], openai_api_key: str = None) -> Dict[str, Any]:
        """
        Gera roteiro para Carrossel (Instagram)
        Formato: 9:16 por slide
        """
        
        tema_refinado = self._refinar_tema(ideia["tema"])
        cta_final = self._gerar_cta_final(ideia["cta"], openai_api_key=openai_api_key)
        
        segmentos = [
            {
                "nome": "Slide 1 - Capa",
                "titulo": "5 Passos para Organizar seu Orçamento",
                "texto_curto": "Método simples e prático",
                "texto_na_tela": "SWIPE PARA VER →",
                "sugestao_visual": "Design limpo com título destacado"
            },
            {
                "nome": "Slide 2 - Passo 1",
                "titulo": "1. ANOTE TUDO",
                "texto_curto": "• Registre cada gasto\n• Use app ou caderno\n• Faça por 1 semana",
                "texto_na_tela": "PASSO 1",
                "sugestao_visual": "Ícone de anotação + bullets"
            },
            {
                "nome": "Slide 3 - Passo 2",
                "titulo": "2. CATEGORIZE",
                "texto_curto": "• Alimentação\n• Transporte\n• Lazer\n• Contas fixas",
                "texto_na_tela": "PASSO 2",
                "sugestao_visual": "Ícones de categorias"
            }
            # Adicionar mais slides conforme necessário
        ]
        
        return {
            "formato": ideia["formato"],
            "canal": ideia["canal"],
            "persona": ideia["persona"],
            "pilar": ideia["pilar"],
            "tema": tema_refinado,
            "kpi_principal": ideia["kpi_principal"],
            "cta_final": cta_final,
            "diretrizes_execucao": {
                "aspect_ratio": "9:16",
                "duracao_alvo_segundos": 0,  # Carrossel não tem duração
                "tom_de_voz": ["didático", "prático", "moderno"],
                "observacoes": self._extrair_observacoes(ideia.get("observacoes", ""))
            },
            "segmentos": segmentos,
            "meta_publicacao": {
                "legenda": f"💰 {tema_refinado}\n\nSalve este post e siga o passo a passo!\n\n{cta_final}\n\n❓ Qual passo você vai começar hoje?",
                "hashtags": ["#educacaofinanceira", "#orcamento", "#dicas"],
                "thumb_titulo": "Organize seu Orçamento"
            },
            "assets_sugeridos": [
                "Template de carrossel limpo",
                "Ícones para cada categoria",
                "Paleta de cores consistente",
                "Tipografia legível"
            ]
        }
    
    def _gerar_roteiro_post_telegram(self, ideia: Dict[str, Any]) -> Dict[str, Any]:
        """
        Gera roteiro para Post Telegram
        """
        
        tema_refinado = self._refinar_tema(ideia["tema"])
        
        post_texto = f"💰 DICA DO DIA: {tema_refinado}\n\n" + \
                    "Hoje vou te ensinar uma técnica simples que pode economizar até R$ 200 por mês no seu orçamento.\n\n" + \
                    "🎯 A TÉCNICA DOS 3 POTES:\n" + \
                    "1️⃣ Pote ESSENCIAL (50% da renda)\n" + \
                    "2️⃣ Pote DIVERSÃO (30% da renda)\n" + \
                    "3️⃣ Pote FUTURO (20% da renda)\n\n" + \
                    "✅ Comece hoje mesmo separando seu dinheiro assim!\n\n" + \
                    "👥 Quer mais dicas como essa? Entre na nossa comunidade gratuita!"
        
        return {
            "formato": ideia["formato"],
            "canal": ideia["canal"],
            "persona": ideia["persona"],
            "pilar": ideia["pilar"],
            "tema": tema_refinado,
            "kpi_principal": ideia["kpi_principal"],
            "cta_final": "Entre na comunidade gratuita do Telegram",
            "diretrizes_execucao": {
                "aspect_ratio": "N/A",
                "duracao_alvo_segundos": 0,
                "tom_de_voz": ["didático", "prático", "acolhedor"],
                "observacoes": self._extrair_observacoes(ideia.get("observacoes", ""))
            },
            "post_texto": post_texto,
            "enquete": {
                "pergunta": "Qual sua maior dificuldade com orçamento?",
                "opcoes": ["Controlar gastos", "Poupar dinheiro", "Organizar contas", "Aumentar renda"]
            },
            "call_to_action": "Entre na comunidade e receba dicas diárias!",
            "resumo_do_dia": "Lembre-se: pequenos ajustes no orçamento geram grandes resultados!",
            "meta_publicacao": {
                "legenda": post_texto,
                "hashtags": ["#educacaofinanceira", "#orcamento", "#telegram"],
                "thumb_titulo": "Técnica dos 3 Potes"
            },
            "assets_sugeridos": [
                "Imagem simples com os 3 potes",
                "Infográfico com percentuais",
                "Sticker de dinheiro"
            ]
        }
    
    def _gerar_roteiro_stories_status(self, ideia: Dict[str, Any]) -> Dict[str, Any]:
        """
        Gera roteiro para Stories/Status (IG/WhatsApp)
        Formato: 9:16, 3 a 5 cards
        """
        
        tema_refinado = self._refinar_tema(ideia["tema"])
        
        segmentos = [
            {
                "nome": "Card 1",
                "texto": "Você gasta mais do que ganha?",
                "narracao": "Se você respondeu sim, este stories é para você!",
                "visual_sugestoes": ["pergunta destacada", "emoji de dinheiro"],
                "sticker_interativo": "enquete: Sim/Não",
                "cta": "Responda a enquete"
            },
            {
                "nome": "Card 2",
                "texto": "REGRA 50-30-20",
                "narracao": "50% essencial, 30% diversão, 20% futuro",
                "visual_sugestoes": ["gráfico simples", "percentuais destacados"],
                "sticker_interativo": "slider: Quanto você poupa?",
                "cta": "Deslize para ver mais"
            },
            {
                "nome": "Card 3",
                "texto": "COMECE HOJE!",
                "narracao": "Separe seu dinheiro em 3 categorias agora mesmo",
                "visual_sugestoes": ["call to action", "seta apontando"],
                "sticker_interativo": "pergunta: Qual sua meta de economia?",
                "cta": "Entre na comunidade para mais dicas"
            }
        ]
        
        return {
            "formato": ideia["formato"],
            "canal": ideia["canal"],
            "persona": ideia["persona"],
            "pilar": ideia["pilar"],
            "tema": tema_refinado,
            "kpi_principal": ideia["kpi_principal"],
            "cta_final": "Entre na comunidade gratuita",
            "diretrizes_execucao": {
                "aspect_ratio": "9:16",
                "duracao_alvo_segundos": 15,
                "tom_de_voz": ["prático", "direto", "moderno"],
                "observacoes": self._extrair_observacoes(ideia.get("observacoes", ""))
            },
            "segmentos": segmentos,
            "meta_publicacao": {
                "legenda": f"💰 {tema_refinado} - Stories com dica rápida!",
                "hashtags": ["#stories", "#educacaofinanceira", "#dicasrapidas"],
                "thumb_titulo": "Dica Rápida de Orçamento"
            },
            "assets_sugeridos": [
                "Templates de stories modernos",
                "Stickers interativos",
                "Paleta de cores vibrante",
                "Tipografia bold para mobile"
            ]
        }
    
    def _aplicar_ajustes_kpi(self, roteiro: Dict[str, Any], kpi: str) -> Dict[str, Any]:
        """
        Aplica ajustes específicos baseados no KPI principal
        """
        
        if kpi == "CTR":
            # CTA no meio e final, reforçar benefício claro
            if "segmentos" in roteiro:
                meio = len(roteiro["segmentos"]) // 2
                if meio < len(roteiro["segmentos"]):
                    # Verificar se o segmento tem 'narracao' (Reel/YouTube) ou 'texto_curto' (Carrossel)
                    if "narracao" in roteiro["segmentos"][meio]:
                        roteiro["segmentos"][meio]["narracao"] += " Link na bio para mais dicas!"
                    elif "texto_curto" in roteiro["segmentos"][meio]:
                        roteiro["segmentos"][meio]["texto_curto"] += "\n• Link na bio!"
        
        elif kpi == "Salvamentos":
            # Checklist em 3 passos e bullets copiáveis
            roteiro["meta_publicacao"]["legenda"] += "\n\n📋 SALVE ESTE POST para não esquecer!"
        
        elif kpi == "Retenção":
            # Open loop no início e variação visual
            if "segmentos" in roteiro and len(roteiro["segmentos"]) > 0:
                primeiro_segmento = roteiro["segmentos"][0]
                primeiro_segmento["narracao"] = "O erro #2 é o mais comum... " + primeiro_segmento["narracao"]
        
        return roteiro
    
    def _gerar_narracao_segmento(self, nome_segmento: str, tema: str, persona: str, 
                                 duracao_s: int, ajustes_kpi: Dict[str, Any], openai_api_key: str = None) -> str:
        """
        Gera narração para um segmento específico usando OpenAI
        """
        if self.openai_disponivel:
            # Construir prompt detalhado para OpenAI
            kpi_instrucoes = ""
            if ajustes_kpi.get("cta_meio") and nome_segmento in ["Passo 2", "Exemplo"]:
                kpi_instrucoes += "Inclua um CTA sutil no meio. "
            if ajustes_kpi.get("pergunta_direta") and nome_segmento == "Hook":
                kpi_instrucoes += "Faça uma pergunta direta ao público. "
            if ajustes_kpi.get("open_loop") and nome_segmento == "Hook":
                kpi_instrucoes += "Crie suspense/curiosidade sem revelar tudo. "
            
            prompt = f"""
            Crie uma narração para o segmento "{nome_segmento}" de um roteiro sobre "{tema}" direcionado para "{persona}".
            
            Duração: {duracao_s} segundos
            Regras de narração:
            - Português do Brasil, linguagem para leigos
            - Frases curtas, verbos de ação
            - Sem jargões técnicos
            - Tom empático e prático
            - Máximo 2-3 frases
            
            {kpi_instrucoes}
            
            Retorne apenas a narração, sem explicações adicionais.
            """
            
            return self._gerar_conteudo_com_openai(prompt, openai_api_key=openai_api_key, max_tokens=150)
        
        # Fallback básico
        templates = {
            "Hook": [
                f"Você sabia que {tema.lower()}? Vou te mostrar como resolver isso.",
                f"Pare tudo! {tema} pode mudar sua vida financeira.",
                f"Atenção: {tema} - vou te ensinar o passo a passo."
            ],
            "Contexto": [
                f"Muitas pessoas enfrentam dificuldades com {tema.lower()}.",
                f"O problema é que {tema.lower()} não é ensinado nas escolas.",
                f"Vamos entender por que {tema.lower()} é tão importante."
            ],
            "Passo": [
                "Primeiro passo: organize suas informações.",
                "Segundo passo: defina suas prioridades.",
                "Terceiro passo: coloque em prática."
            ],
            "CTA": [
                "Quer aprender mais? Entre na nossa comunidade gratuita!",
                "Gostou do conteúdo? Compartilhe com quem precisa!",
                "Tem dúvidas? Comenta aqui embaixo!"
            ]
        }
        
        opcoes = templates.get(nome_segmento, templates["Passo"])
        narracao_base = opcoes[0]
        
        # Aplicar ajustes de KPI
        if ajustes_kpi.get("cta_meio") and nome_segmento in ["Passo 2", "Exemplo"]:
            narracao_base += " Quer ver mais dicas como essa?"
        
        if ajustes_kpi.get("pergunta_direta") and nome_segmento == "Hook":
            narracao_base = narracao_base.replace("Você sabia", "Você já passou por isso")
        
        return narracao_base
    
    def _gerar_conteudo_com_openai(self, prompt: str, openai_api_key: str = None, max_tokens: int = 1000) -> str:
        """
        Gera conteúdo usando a API da OpenAI
        
        Args:
            prompt: Prompt para geração de conteúdo
            openai_api_key: Chave da API OpenAI (não armazenada)
            max_tokens: Número máximo de tokens
            
        Returns:
            Conteúdo gerado ou fallback básico
        """
        # Usar chave fornecida ou fallback para sessão atual
        api_key = openai_api_key or self._openai_key_for_session
        
        if not api_key or not openai:
            return self._gerar_conteudo_basico(prompt)
        
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "Você é um especialista em educação financeira e roteirista de conteúdo. Crie conteúdo didático, empático e prático em português do Brasil para pessoas leigas em finanças. Use frases curtas, verbos de ação e evite jargões técnicos."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=max_tokens,
                temperature=0.7,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Erro ao usar OpenAI: {e}")
            return self._gerar_conteudo_basico(prompt)
    
    def _gerar_visual_segmento(self, nome_segmento: str, tema: str, narracao: str, openai_api_key: str = None) -> List[str]:
        """
        Gera sugestões visuais para um segmento usando OpenAI
        """
        # Verificar se OpenAI está disponível
        api_key = openai_api_key or self._openai_key_for_session
        if api_key and openai:
            prompt = f"""
            Sugira elementos visuais para um segmento "{nome_segmento}" sobre "{tema}".
            
            Narração: "{narracao}"
            
            Regras para elementos visuais:
            - Use categorias genéricas (ex: "ícone de orçamento", "gráfico simples")
            - NUNCA use fotos identificáveis ou dados pessoais
            - Foque em ilustrações, ícones e gráficos simples
            - Máximo 3 sugestões
            - Seja específico mas genérico (ex: "tipografia cinética com números")
            
            Retorne apenas uma lista de 2-3 elementos visuais separados por vírgula.
            """
            
            resposta = self._gerar_conteudo_com_openai(prompt, openai_api_key=openai_api_key, max_tokens=100)
            visuais = [v.strip() for v in resposta.split(',') if v.strip()]
            return visuais[:3]  # Garantir máximo 3
        
        # Fallback básico
        visuais_base = {
            "Hook": ["tipografia cinética", "ícone chamativo"],
            "Contexto": ["gráfico simples", "ilustração conceitual"],
            "Passo": ["ícone de passo", "bullet point"],
            "Exemplo": ["mockup de tela", "ilustração prática"],
            "CTA": ["botão de ação", "seta indicativa"]
        }
        
        # Adicionar visuais específicos baseados no tema
        visuais_tema = []
        if "orçamento" in tema.lower():
            visuais_tema.extend(["ícone de orçamento", "planilha simples"])
        elif "investimento" in tema.lower():
            visuais_tema.extend(["gráfico de crescimento", "ícone de investimento"])
        elif "economia" in tema.lower():
            visuais_tema.extend(["cofre", "moedas"])
        
        # Combinar visuais base com específicos do tema
        visuais = visuais_base.get(nome_segmento, ["ícone genérico"])
        if visuais_tema:
            visuais.extend(visuais_tema[:2])  # Máximo 2 visuais adicionais
        
        return visuais[:3]  # Máximo 3 sugestões visuais
    
    def _gerar_musica_segmento(self, nome_segmento: str, tema: str, narracao: str, openai_api_key: str = None) -> Dict[str, str]:
        """
        Gera sugestões de música para um segmento usando OpenAI
        """
        # Verificar se OpenAI está disponível
        api_key = openai_api_key or self._openai_key_for_session
        if api_key and openai:
            prompt = f"""
            Sugira música/áudio para um segmento "{nome_segmento}" sobre "{tema}".
            
            Narração: "{narracao}"
            
            Regras para música:
            - Especifique apenas mood e BPM
            - NUNCA sugira músicas comerciais específicas
            - Prefira biblioteca sem direitos/livre de royalties
            - Inclua SFX sutis quando apropriado (whoosh, click, etc.)
            
            Retorne no formato: mood: [mood], bpm: [faixa], sfx: [efeito opcional]
            """
            
            resposta = self._gerar_conteudo_com_openai(prompt, openai_api_key=openai_api_key, max_tokens=80)
            
            # Parse da resposta
            musica = {"mood": "otimista", "bpm": "100-110", "tipo": "biblioteca sem direitos"}
            sfx = []
            
            if "mood:" in resposta:
                mood_start = resposta.find("mood:") + 5
                mood_end = resposta.find(",", mood_start)
                if mood_end == -1:
                    mood_end = resposta.find("\n", mood_start)
                if mood_end == -1:
                    mood_end = len(resposta)
                musica["mood"] = resposta[mood_start:mood_end].strip()
            
            if "bpm:" in resposta:
                 bpm_start = resposta.find("bpm:") + 4
                 bpm_end = resposta.find(",", bpm_start)
                 if bpm_end == -1:
                     bpm_end = resposta.find("\n", bpm_start)
                 if bpm_end == -1:
                     bpm_end = len(resposta)
                 musica["bpm"] = resposta[bpm_start:bpm_end].strip()
            
            if "sfx:" in resposta:
                sfx_start = resposta.find("sfx:") + 4
                sfx_text = resposta[sfx_start:].strip()
                if sfx_text and sfx_text != "nenhum":
                    sfx = [sfx_text]
            
            return {"musica_sugestao": musica, "sfx_sugestao": sfx}
        
        # Fallback básico
        musicas_base = {
            "Hook": {"mood": "empolgante", "bpm": "110-120"},
            "Contexto": {"mood": "reflexivo", "bpm": "80-90"},
            "Passo": {"mood": "focado", "bpm": "95-105"},
            "Exemplo": {"mood": "prático", "bpm": "100-110"},
            "CTA": {"mood": "convidativo", "bpm": "100-110"}
        }
        
        musica = musicas_base.get(nome_segmento, {"mood": "otimista", "bpm": "100-110"})
        musica["tipo"] = "biblioteca sem direitos"
        
        sfx_base = {
            "Hook": ["whoosh"],
            "Passo": ["click suave"],
            "CTA": ["chime"]
        }
        
        sfx = sfx_base.get(nome_segmento, [])
        
        return {"musica_sugestao": musica, "sfx_sugestao": sfx}
    
    def _gerar_conteudo_basico(self, prompt: str) -> str:
        """
        Gera conteúdo básico quando OpenAI não está disponível
        """
        # Implementação básica de fallback
        if "narração" in prompt.lower():
            return "Vamos aprender sobre educação financeira de forma prática e simples."
        elif "visual" in prompt.lower():
            return "ícone de dinheiro, gráfico simples"
        elif "música" in prompt.lower():
            return "otimista, 100-110 BPM"
        else:
            return "Conteúdo educativo sobre finanças pessoais."
    
    def _refinar_tema(self, tema_original: str) -> str:
        """
        Refina o tema mantendo dor/desejo explícitos (máx. ~90 caracteres)
        """
        
        if len(tema_original) <= 90:
            return tema_original
        
        # Simplificar mantendo a essência
        palavras = tema_original.split()
        tema_refinado = ""
        
        for palavra in palavras:
            if len(tema_refinado + palavra + " ") <= 90:
                tema_refinado += palavra + " "
            else:
                break
        
        return tema_refinado.strip()
    
    def _gerar_cta_final(self, cta_tipo: str, openai_api_key: str = None) -> str:
        """
        Gera o texto do CTA final baseado no tipo usando OpenAI
        """
        # Verificar se OpenAI está disponível
        api_key = openai_api_key or self._openai_key_for_session
        if api_key and openai:
            prompt = f"""
            Crie um CTA (Call to Action) para "{cta_tipo}".
            
            Regras para CTA:
            - Seja direto e convidativo
            - Use verbos de ação
            - Mencione benefício claro
            - Tom acolhedor, não agressivo
            - Máximo 2 frases
            - Português do Brasil
            
            Retorne apenas o CTA, sem explicações adicionais.
            """
            
            return self._gerar_conteudo_com_openai(prompt, openai_api_key=openai_api_key, max_tokens=100)
        
        # Fallback básico
        ctas = {
            "Comunidade Telegram": "Entre na nossa comunidade gratuita do Telegram e receba dicas diárias!",
            "WhatsApp Diagnóstico": "Faça seu diagnóstico financeiro gratuito em 5 minutos no WhatsApp!",
            "Download Planilha": "Baixe nossa planilha gratuita de controle financeiro!",
            "Curso Gratuito": "Inscreva-se no nosso curso gratuito de educação financeira!"
        }
        
        return ctas.get(cta_tipo, "Entre na nossa comunidade gratuita do Telegram!")
    
    def _extrair_observacoes(self, observacoes: str) -> str:
        """
        Extrai e resume as observações úteis
        """
        
        if not observacoes:
            return "Foco em ação prática e linguagem simples"
        
        # Extrair dor e desejo se mencionados
        resumo = ""
        if "dor:" in observacoes.lower():
            inicio_dor = observacoes.lower().find("dor:")
            fim_dor = observacoes.find("|", inicio_dor) if "|" in observacoes[inicio_dor:] else len(observacoes)
            dor = observacoes[inicio_dor:fim_dor].strip()
            resumo += dor + " "
        
        if "desejo:" in observacoes.lower():
            inicio_desejo = observacoes.lower().find("desejo:")
            fim_desejo = observacoes.find("|", inicio_desejo) if "|" in observacoes[inicio_desejo:] else len(observacoes)
            desejo = observacoes[inicio_desejo:fim_desejo].strip()
            resumo += desejo
        
        return resumo.strip() if resumo.strip() else "Foco em ação prática e linguagem simples"


def processar_roteiro(ideia_revisada_json: str, openai_api_key: str = None) -> str:
    """
    Função principal para processar uma ideia revisada e retornar o roteiro em JSON
    
    Args:
        ideia_revisada_json: String JSON com a ideia revisada
        openai_api_key: Chave da API OpenAI (opcional)
        
    Returns:
        String JSON com o roteiro completo
    """
    
    try:
        # Parse da entrada
        ideia_revisada = json.loads(ideia_revisada_json)
        
        # Criar instância do roteirista com chave da API
        roteirista = FinanceIARoteirista(openai_api_key=openai_api_key)
        
        # Processar ideia e gerar roteiro
        resultado = roteirista.processar_ideia_revisada(ideia_revisada, openai_api_key=openai_api_key)
        
        # Retornar JSON
        return json.dumps(resultado, ensure_ascii=False, indent=2)
        
    except Exception as e:
        return json.dumps({
            "erro": f"Erro ao processar roteiro: {str(e)}",
            "status": "erro"
        }, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    # Exemplo de uso
    exemplo_ideia = {
        "data_da_semana": "2024-01-15",
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
    
    resultado = processar_roteiro(json.dumps(exemplo_ideia))
    print(resultado)