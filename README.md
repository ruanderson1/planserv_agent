# 📱 planserv - Agente de IA via WhatsApp

Este projeto é um agente inteligente que interage com usuários via WhatsApp, utilizando **Flask**, **Twilio** e **modelos de IA (OpenAI/Gemini)**.  
Abaixo está a explicação da estrutura de pastas e dos principais componentes do projeto.

---

## 📁 Estrutura de Pastas

```
planserv_project/
│
├── app/
│   ├── routes/
│   ├── services/
│   ├── utils/
│   ├── models/
│   └── static/
│
├── tests/
├── .env
├── requirements.txt
├── README.md
└── run.py
```

---

## 📦 Descrição das Pastas Principais

### `app/routes/`

Contém as rotas (endpoints) da aplicação Flask, incluindo as integrações com o Twilio (para WhatsApp) e outras APIs.

### `app/services/`

Responsável pela lógica de negócio e integrações externas — como comunicação com APIs de IA (OpenAI, Gemini) e envio de mensagens via Twilio.

### `app/utils/`

Inclui funções auxiliares como logs, leitura de variáveis do `.env` e formatação de dados.

### `app/models/`

Define estruturas de dados e classes utilizadas na aplicação (ex: mensagens e usuários).

### `app/static/`

Armazena arquivos estáticos, como áudios gerados, ícones e imagens.

### `tests/`

Contém testes automatizados para verificar o funcionamento das rotas e serviços.

### `.env`

Arquivo de configuração com variáveis de ambiente (tokens, chaves e credenciais).

### `requirements.txt`

Lista de dependências Python do projeto.

### `run.py`

Arquivo principal para iniciar o servidor Flask.

---

## 🚀 Como Executar

1. Clone o repositório:

   ```bash
   git clone...
   entre na pasta planserv_project
   ```

2. Crie o ambiente virtual e instale as dependências:

   ```bash
   python -m venv venv
   source venv/bin/activate  # ou venv\Scripts\activate no Windows
   pip install -r requirements.txt
   ```

3. Configure o arquivo `.env` com suas credenciais.

4. Inicie o servidor Flask:

   ```bash
    cd planserve_project
    py -m app.main
   ```

5. Realizar testes

   ```bash
    cd planserve_project
    cd tests
    pytest -v

   ```

---
