#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Finance-IA - Configurações do Sistema de Roteirização
Contém todas as listas válidas e configurações do sistema
"""

# Listas válidas para validação de entrada
LISTAS_VALIDAS = {
    "personas": [
        "Jovem Adulto",
        "Casal", 
        "Família",
        "Empreendedor",
        "Aposentado"
    ],
    
    "pilares": [
        "Orçamento",
        "Investimentos", 
        "Dívidas",
        "Renda Extra",
        "Planejamento"
    ],
    
    "formatos": [
        "Reel/Short",
        "YouTube Longo",
        "Carrossel", 
        "Post Telegram",
        "Stories/Status"
    ],
    
    "canais": [
        "Instagram",
        "TikTok",
        "YouTube",
        "Telegram",
        "WhatsApp"
    ],
    
    "ctas": [
        "Comunidade Telegram",
        "WhatsApp Diagnóstico",
        "Download Planilha",
        "Curso Gratuito"
    ],
    
    "kpis": [
        "CTR",
        "Salvamentos",
        "Retenção", 
        "Engajamento",
        "Conversão"
    ],
    
    "prioridade": [
        "Alta",
        "Média",
        "Baixa"
    ]
}

# Configurações de formato por tipo de conteúdo
CONFIGURACOES_FORMATO = {
    "Reel/Short": {
        "aspect_ratio": "9:16",
        "duracao_min": 20,
        "duracao_max": 45,
        "segmentos_obrigatorios": ["Hook", "Passo 1", "Passo 2", "Passo 3", "Prova visual", "CTA final"]
    },
    
    "YouTube Longo": {
        "aspect_ratio": "16:9",
        "duracao_min": 480,  # 8 minutos
        "duracao_max": 720,  # 12 minutos
        "capitulos_obrigatorios": ["Hook", "Contexto", "Passo a passo", "Exemplo aplicado", "Erros comuns", "CTA final"]
    },
    
    "Carrossel": {
        "aspect_ratio": "9:16",
        "slides_min": 6,
        "slides_max": 10,
        "estrutura": ["Capa", "Passos", "Erro comum", "CTA"]
    },
    
    "Post Telegram": {
        "caracteres_max": 1200,
        "elementos": ["post_texto", "enquete", "call_to_action", "resumo_do_dia"]
    },
    
    "Stories/Status": {
        "aspect_ratio": "9:16",
        "cards_min": 3,
        "cards_max": 5,
        "duracao_por_card": 5
    }
}

# Regras de narração
REGRAS_NARRACAO = {
    "idioma": "português do Brasil",
    "publico_alvo": "leigos em educação financeira",
    "estilo": {
        "frases": "curtas e diretas",
        "verbos": "de ação",
        "jargoes": "evitar completamente",
        "termos_tecnicos": "explicar em 1 linha quando necessário"
    },
    "tom_de_voz": [
        "didático",
        "empático", 
        "prático",
        "confiável",
        "moderno",
        "inspirador"
    ]
}

# Regras para elementos visuais
REGRAS_VISUAL = {
    "tipo_permitido": "categorias genéricas",
    "exemplos_bons": [
        "ícone de orçamento",
        "gráfico simples", 
        "mãos ajustando planilha",
        "calculadora",
        "gráfico de pizza",
        "ícones de categorias"
    ],
    "proibido": [
        "fotos que identifiquem pessoas",
        "dados pessoais visíveis",
        "prints com informações privadas",
        "rostos identificáveis",
        "documentos reais"
    ]
}

# Regras para música e áudio
REGRAS_MUSICA = {
    "especificar_sempre": ["mood", "bpm"],
    "tipo_preferido": "biblioteca sem direitos/livre de royalties",
    "proibido": "músicas comerciais específicas",
    "sfx": {
        "estilo": "sutil",
        "exemplos": ["whoosh", "click", "ding", "chime"]
    },
    "moods_comuns": [
        "otimista",
        "focado",
        "inspirador",
        "empático",
        "determinado",
        "convidativo"
    ]
}

# Ajustes automáticos por KPI
AJUSTES_KPI = {
    "CTR": {
        "estrategia": "CTA no meio e final, reforçar benefício claro",
        "implementacao": "adicionar_cta_meio_video"
    },
    
    "Salvamentos": {
        "estrategia": "checklist em 3 passos e bullets copiáveis",
        "implementacao": "formato_checklist_bullets"
    },
    
    "Retenção": {
        "estrategia": "open loop no início, variação visual a cada 3-5s",
        "implementacao": "open_loop_inicio_variacao_visual"
    },
    
    "Engajamento": {
        "estrategia": "perguntas diretas, enquetes, call to action para comentar",
        "implementacao": "elementos_interativos"
    },
    
    "Conversão": {
        "estrategia": "benefício claro, urgência sutil, CTA específico",
        "implementacao": "foco_conversao"
    }
}

# Regras LGPD e ética
REGRAS_LGPD_ETICA = {
    "dados_proibidos": [
        "nomes completos",
        "telefones", 
        "CPFs",
        "valores bancários reais",
        "prints com PII (Informações Pessoais Identificáveis)"
    ],
    
    "promessas_proibidas": [
        "garantido",
        "fique rico", 
        "100% certo",
        "sem risco",
        "dinheiro fácil",
        "enriquecimento rápido"
    ],
    
    "tom_obrigatorio": {
        "estilo": "acolhedor e não-julgador",
        "foco": "1 ação prática aplicável hoje",
        "abordagem": "educativa e responsável"
    }
}

# Templates de CTA por tipo
TEMPLATES_CTA = {
    "Comunidade Telegram": {
        "texto_curto": "Entre na comunidade gratuita!",
        "texto_completo": "Entre na nossa comunidade gratuita do Telegram e receba dicas diárias de educação financeira!",
        "prioridade": 1
    },
    
    "WhatsApp Diagnóstico": {
        "texto_curto": "Faça seu diagnóstico gratuito!",
        "texto_completo": "Faça seu diagnóstico financeiro gratuito em 5 minutos no WhatsApp!",
        "prioridade": 2,
        "condicao": "quando houver entrega imediata"
    },
    
    "Download Planilha": {
        "texto_curto": "Baixe a planilha gratuita!",
        "texto_completo": "Baixe nossa planilha gratuita de controle financeiro e organize suas contas hoje mesmo!",
        "prioridade": 3
    },
    
    "Curso Gratuito": {
        "texto_curto": "Inscreva-se no curso gratuito!",
        "texto_completo": "Inscreva-se no nosso curso gratuito de educação financeira e transforme sua vida financeira!",
        "prioridade": 4
    }
}

# Hashtags por pilar
HASHTAGS_POR_PILAR = {
    "Orçamento": [
        "#educacaofinanceira",
        "#orcamento", 
        "#controlefinanceiro",
        "#economia",
        "#dinheiro",
        "#financas"
    ],
    
    "Investimentos": [
        "#educacaofinanceira",
        "#investimentos",
        "#rendapassiva", 
        "#investir",
        "#dinheiro",
        "#financas"
    ],
    
    "Dívidas": [
        "#educacaofinanceira",
        "#dividas",
        "#quitardividas",
        "#controlefinanceiro",
        "#organizacaofinanceira",
        "#financas"
    ],
    
    "Renda Extra": [
        "#educacaofinanceira",
        "#rendaextra",
        "#empreendedorismo",
        "#dinheiro",
        "#oportunidades",
        "#financas"
    ],
    
    "Planejamento": [
        "#educacaofinanceira",
        "#planejamentofinanceiro",
        "#metas",
        "#objetivos",
        "#futuro",
        "#financas"
    ]
}

# Configurações de exportação
CONFIG_EXPORTACAO = {
    "formato_data": "%Y-%m-%d",
    "encoding": "utf-8",
    "indent_json": 2,
    "ensure_ascii": False
}