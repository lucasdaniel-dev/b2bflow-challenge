# b2bflow Challenge — WhatsApp Notifier

Projeto desenvolvido como parte do processo seletivo para **Estágio em Desenvolvimento Python** na [b2bflow](https://b2bflow.com.br).

O script lê contatos cadastrados no **Supabase** e envia, via **Z-API**, a mensagem personalizada:

> *"Olá, `<nome_contato>` tudo bem com você?"*

---

## Tecnologias

- Python 3.11+
- [Supabase](https://supabase.com) — banco de dados (PostgreSQL gerenciado)
- [Z-API](https://z-api.io) — envio de mensagens via WhatsApp
- `python-dotenv`, `requests`, `supabase-py`

---

## Estrutura do Projeto

```
b2bflow-challenge/
├── main.py                  # Ponto de entrada
├── services/
│   ├── supabase_client.py   # Leitura de contatos no Supabase
│   └── zapi_client.py       # Envio de mensagens via Z-API
├── .env.example             # Modelo de variáveis de ambiente
├── requirements.txt
└── README.md
```

---

## Setup

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/b2bflow-challenge.git
cd b2bflow-challenge
```

### 2. Crie e ative um ambiente virtual

```bash
python -m venv .venv
source .venv/bin/activate        # Linux/Mac
.venv\Scripts\activate           # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas credenciais (veja a seção abaixo).

---

## Configuração do Supabase

1. Acesse [supabase.com](https://supabase.com) e crie um projeto gratuito.
2. No **Table Editor**, crie a tabela `contacts` com as colunas:

| Coluna  | Tipo    | Obrigatório |
|---------|---------|-------------|
| `id`    | `int8`  | ✅ (PK, auto) |
| `name`  | `text`  | ✅ |
| `phone` | `text`  | ✅ |

3. Insira até 3 contatos de teste.
4. Em **Project Settings → API**, copie a **URL** e a chave **anon/public**.

---

## Configuração da Z-API

1. Acesse [z-api.io](https://z-api.io) e crie uma conta gratuita.
2. Crie uma instância e conecte seu WhatsApp via QR Code.
3. No painel da instância, copie o **Instance ID**, o **Token** e o **Client-Token** (Security → Client Token).

---

## Variáveis de Ambiente (`.env`)

```env
# Supabase
SUPABASE_URL=https://xxxxxxxxxxx.supabase.co
SUPABASE_KEY=your_anon_public_key_here
SUPABASE_TABLE=contacts

# Z-API
ZAPI_INSTANCE_ID=your_instance_id
ZAPI_TOKEN=your_token
ZAPI_CLIENT_TOKEN=your_client_token
```

> ⚠️ O arquivo `.env` **nunca** deve ser commitado. Ele já está no `.gitignore`.

---

## Como Rodar

```bash
python main.py
```

**Exemplo de saída esperada:**

```
2025-06-19 10:00:00 [INFO] 🚀 Iniciando envio de mensagens via WhatsApp...
2025-06-19 10:00:01 [INFO] 3 contato(s) encontrado(s). Iniciando envios...
2025-06-19 10:00:02 [INFO] ✅ Mensagem enviada para João (5511999990001)
2025-06-19 10:00:03 [INFO] ✅ Mensagem enviada para Maria (5511999990002)
2025-06-19 10:00:04 [INFO] ✅ Mensagem enviada para Carlos (5511999990003)
2025-06-19 10:00:04 [INFO] Concluído. ✅ 3 enviado(s) | ❌ 0 falha(s).
```

---

## Boas Práticas Adotadas

- Separação em camadas (`services/`) para facilitar manutenção e testes
- Variáveis sensíveis isoladas em `.env` (nunca hardcoded)
- Tratamento explícito de erros HTTP, timeout e conexão
- Logs estruturados com nível e timestamp
- Normalização automática do número de telefone (adiciona DDI 55)
- Tipagem estática com type hints
