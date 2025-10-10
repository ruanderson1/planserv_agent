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
   git clone https://github.com/ruanderson1/planserv_agent.git
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
    py run.py
   ```

   OU

   ```bash
    cd planserve_project
    py -m app.main
   ```

5. Realizar testes

   com pytest

   ```bash
    cd planserve_project
    cd tests
    pytest -v
   ```

   Com logs

   ```bash
   cd planserve_project
   cd tests
   py api_query_test.py
   ```

6. ## Padrão de Commits

Para manter o histórico do projeto organizado, utilize o seguinte padrão de commits:

### Formato

### Tipos principais

| Tipo       | Uso                                                | Exemplo                                               |
| ---------- | -------------------------------------------------- | ----------------------------------------------------- |
| `feat`     | Nova funcionalidade ou recurso                     | `feat(auth): adicionar login via WhatsApp`            |
| `fix`      | Correção de bug                                    | `fix(api): corrigir endpoint de leads`                |
| `docs`     | Alteração em documentação                          | `docs: atualizar README.md`                           |
| `style`    | Formatação, espaços, ponto e vírgula, etc.         | `style: padronizar indentação no app/routes`          |
| `refactor` | Refatoração de código sem adicionar funcionalidade | `refactor(services): melhorar leitura do LeadService` |
| `test`     | Adição ou ajuste de testes                         | `test(api): adicionar teste de fluxo completo`        |
| `chore`    | Tarefas de manutenção, configs, scripts            | `chore: atualizar dependências do requirements.txt`   |

### Boas práticas

1. Use inglês consistente em todo o projeto.
2. Limite a descrição curta a 50 caracteres.
3. Inclua escopo opcional para especificar a área afetada (`auth`, `api`, `db`, `services`).
4. Use o corpo do commit para explicar o “porquê” da mudança, se necessário.
5. Use `BREAKING CHANGE:` no rodapé para mudanças que quebram compatibilidade.

---
