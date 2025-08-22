# 🎬 Finance-IA - Agente Roteirista

> Sistema automatizado para gerar roteiros prontos para produção de conteúdo de educação financeira

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)](https://flask.palletsprojects.com)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-orange.svg)](https://openai.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📋 Índice

- [Visão Geral](#-visão-geral)
- [Instalação](#-instalação)
- [Configuração](#-configuração)
- [API Endpoints](#-api-endpoints)
- [Formatos Suportados](#-formatos-suportados)
- [Deploy](#-deploy)
- [Contribuição](#-contribuição)

## 🎯 Visão Geral

O **Finance-IA Agente Roteirista** é uma API REST que gera roteiros completos para conteúdo de educação financeira usando inteligência artificial. O sistema integra-se com OpenAI GPT-4 para criar conteúdo de alta qualidade, mas também funciona em modo básico sem IA.

### ✨ Principais Funcionalidades

- 🤖 **Integração OpenAI GPT-4** - Geração inteligente de conteúdo
- 📱 **Múltiplos Formatos** - Reel, YouTube, Carrossel, Telegram, Stories
- 🎯 **Otimização por KPI** - CTR, Salvamentos, Retenção, Engajamento
- 🔒 **Segurança** - Autenticação por token, validação de chaves API
- 🌐 **API REST** - Endpoints documentados e fáceis de integrar
- 📊 **Modo Fallback** - Funciona sem OpenAI em modo básico

## 🚀 Instalação

### Pré-requisitos

- Python 3.8 ou superior
- Chave da API OpenAI (opcional, para modo inteligente)

### Instalação Local

```bash
# Clone o repositório
git clone https://github.com/marvin-ds/roteirista.git
cd roteirista

# Crie um ambiente virtual
python -m venv .venv

# Ative o ambiente virtual
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate

# Instale as dependências
pip install -r requirements.txt
```

## ⚙️ Configuração

### Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
# Configurações da API
PORT=5000
AUTH_TOKEN=seu-token-de-autenticacao

# OpenAI (opcional)
OPENAI_API_KEY=sua-chave-openai

# Configurações de produção
FLASK_ENV=production
```

### Executar o Servidor

```bash
# Desenvolvimento
python app.py

# Produção com Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 📡 API Endpoints

Todos os endpoints requerem autenticação via header `Authorization: Bearer <token>`.

### 🔍 Health Check

```http
GET /healthz
```

Verifica se o serviço está funcionando.

**Resposta:**
```json
{
  "status": "healthy",
  "service": "finance-ia-roteirista",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### 🎬 Processar Roteiro

```http
POST /processar
Content-Type: application/json
Authorization: Bearer <seu-token>
X-OPENAI-API-KEY: <sua-chave-openai> (opcional)
```

**Corpo da Requisição:**
```json
{
  "data_da_semana": "2024-01-15",
  "tema": "Como criar um orçamento familiar",
  "persona": "Casal",
  "pilar": "Orçamento",
  "formato": "Reel/Short",
  "canal": "Instagram",
  "cta": "Comunidade Telegram",
  "kpi_principal": "CTR",
  "status": "Ideia",
  "lgpd_ok": "Sim",
  "prioridade": "Alta",
  "observacoes": "Foco em casais jovens",
  "openai_api_key": "sk-..." // opcional
}
```

**Resposta:**
```json
{
  "roteiro": {
    "titulo": "Como Criar um Orçamento que Funciona",
    "formato": "Reel/Short",
    "duracao_estimada": "30-45 segundos",
    "trechos": [
      {
        "tempo": "0-5s",
        "tipo": "abertura",
        "naracao": "Você sabe por que 70% dos casais brigam por dinheiro?",
        "visual": "Casal discutindo, transição para casal sorrindo",
        "musica": "Tensão inicial, depois otimista"
      }
    ],
    "cta": {
      "texto": "Entre no nosso Telegram e receba planilhas gratuitas!",
      "posicao": "final"
    }
  },
  "metadata": {
    "gerado_com_ia": true,
    "timestamp": "2024-01-15T10:30:00Z",
    "versao": "1.0"
  }
}
```

### ✅ Validar Dados

```http
POST /validar
Content-Type: application/json
Authorization: Bearer <seu-token>
```

Valida os dados de entrada antes do processamento.

### 📋 Listas Válidas

```http
GET /listas
Authorization: Bearer <seu-token>
```

Retorna todas as opções válidas para os campos.

### 📄 Template

```http
GET /template
Authorization: Bearer <seu-token>
```

Retorna um template de dados para facilitar a integração.

### 🧪 Debug

```http
POST /test-debug
Content-Type: application/json
```

Endpoint para testes (não requer autenticação).

## 🎯 Formatos Suportados

| Formato | Canal | Duração | Proporção | Características |
|---------|-------|---------|-----------|----------------|
| **Reel/Short** | Instagram, TikTok, YouTube | 20-45s | 9:16 | Dinâmico, visual |
| **YouTube Longo** | YouTube | 8-12 min | 16:9 | Educativo, detalhado |
| **Carrossel** | Instagram | 5-10 slides | 9:16 | Informativo, sequencial |
| **Post Telegram** | Telegram | - | - | Texto até 1200 chars |
| **Stories/Status** | Instagram, WhatsApp | 3-5 cards | 9:16 | Rápido, interativo |

## 🎯 Otimização por KPI

- **CTR (Click-Through Rate)**: CTA no meio e final, benefício claro
- **Salvamentos**: Checklist em 3 passos, bullets copiáveis  
- **Retenção**: Open loop no início, variação visual
- **Engajamento**: Perguntas diretas, elementos interativos
- **Conversão**: Benefício claro, urgência sutil

## 🚀 Deploy

### Deploy Local

```bash
# Clonar e configurar
git clone https://github.com/marvin-ds/roteirista.git
cd roteirista
pip install -r requirements.txt

# Configurar variáveis
export AUTH_TOKEN="seu-token-seguro"
export OPENAI_API_KEY="sua-chave-openai"

# Executar
python app.py
```

### Deploy com Docker

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

```bash
# Build e run
docker build -t finance-ia-roteirista .
docker run -p 5000:5000 \
  -e AUTH_TOKEN="seu-token" \
  -e OPENAI_API_KEY="sua-chave" \
  finance-ia-roteirista
```

### Deploy em Produção

**Heroku:**
```bash
# Criar Procfile
echo "web: gunicorn -w 4 -b 0.0.0.0:\$PORT app:app" > Procfile

# Deploy
heroku create seu-app-name
heroku config:set AUTH_TOKEN="seu-token"
heroku config:set OPENAI_API_KEY="sua-chave"
git push heroku main
```

**Railway/Render:**
- Configure as variáveis de ambiente
- Use o comando: `gunicorn -w 4 -b 0.0.0.0:$PORT app:app`

### Monitoramento

```bash
# Health check
curl -H "Authorization: Bearer seu-token" \
  https://seu-dominio.com/healthz

# Logs
tail -f logs/app.log
```

## 🔒 Segurança

### Autenticação

- **Token obrigatório**: Todos os endpoints (exceto `/test-debug`) requerem `Authorization: Bearer <token>`
- **Chave OpenAI**: Pode ser enviada via header `X-OPENAI-API-KEY`, corpo da requisição ou variável de ambiente
- **Mascaramento**: Chaves são mascaradas nos logs (mostra apenas 4 últimos caracteres)

### Boas Práticas

- Use HTTPS em produção
- Mantenha tokens e chaves em variáveis de ambiente
- Monitore logs para tentativas de acesso não autorizado
- Implemente rate limiting se necessário

## 🤝 Contribuição

Contribuições são bem-vindas! Por favor:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

### Desenvolvimento

```bash
# Setup desenvolvimento
git clone https://github.com/marvin-ds/roteirista.git
cd roteirista
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou .venv\Scripts\activate  # Windows
pip install -r requirements.txt

# Executar testes
python -m pytest

# Executar servidor de desenvolvimento
python app.py
```

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 📞 Suporte

Para suporte e dúvidas:

- 🐛 **Issues**: [GitHub Issues](https://github.com/marvin-ds/roteirista/issues)
- 📧 **Email**: Abra uma issue no GitHub
- 📖 **Documentação**: Este README contém toda a documentação necessária

---

**Finance-IA Roteirista** - Transformando ideias em roteiros profissionais com inteligência artificial. 🎬✨