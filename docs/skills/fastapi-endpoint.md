# Skill: Criação de Endpoints / Controllers (FastAPI)

> **Objetivo:** Você (Claude CLI) foi invocado como um Agente de Borda (Edge Layer). Seu papel é injetar os adaptadores e casos de uso já criados nas rotas REST do FastAPI, lidando com autenticação e serialização JSON. 

## 🛠 Contexto Limitado (Zero-Conflict)
Você tem permissão para ler e editar APENAS os arquivos nestes diretórios:
* `/src/api/` (Rotas, Schemas de Input/Output Pydantic, Dependências FastAPI)
* `/tests/integration/api/` (Testes e2e dos endpoints)

## 📋 Passos Secretos (Checklist do Operário)
1. **Modelos Pydantic:** Defina os schemas HTTP de `Request` e `Response` no local adequado (`/src/api/schemas/` ou no topo do arquivo da rota). Validações rigorosas devem acontecer aqui (tipos e range HTTP).
2. **Injeção de Dependências (DI):** Na dependência da rota (ex: `get_create_appointment_usecase`), faça a injeção manual. Importe o repositório real de infra (ex: `SupabaseAppointmentRepository`) e passe-o para o Caso de Uso.
3. **Mapeamento de Erros:** O Endpoint (Rota) NUNCA deve retornar erro 500 para regras de negócio (ex: o `SlotAlreadyLockedError` que recebemos do caso de uso). Capture a exceção do domínio no bloco try/except e retorne os devidos HTTP status codes (HTTP 409 Conflict para o lock).
4. **Testes do Endpoint (TDD):** Crie testes em `/tests/integration/api/` usando o `TestClient` do FastAPI para chamar a rota `/agendamentos` simulando requests de falha e de sucesso (com mocks do UseCase/Repository, se preferir isolar, ou banco de teste).
5. **Auditoria:** Rode os testes (ex: `pytest tests/integration/api/ -v`).

## 🛑 Condição de Saída
Assim que a rota e testes funcionarem, imprima no terminal:
**"✅ SKILL CONCLUÍDA: Endpoint REST implementado e Dependency Injection montada. Hand-off liberado em docs/audits/."** 
Crie o arquivo de audit usando as regras de Handoff estritas e sinalize Trilha Livre para a próxima ação de código.
