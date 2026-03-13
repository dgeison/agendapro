# Plano de Execução: 003 - Camada de Entrada (FastAPI)

> 🏗️ **AUTORIA: IA ESTRATÉGICA (ARQUITETO/GEMINI)**
> *Atenção IA Executora (Claude/Cursor): Este plano é a sua única fonte da verdade. Você não tem autoridade para modificar as fronteiras de domínio ou a arquitetura (Ports & Adapters) definida abaixo. A sua única missão é codificar exatamente o que está aqui.*

## 1. Objetivo do Negócio
Expor o `CreateSessionUseCase` (Domínio) para o mundo externo via uma API HTTP utilizando FastAPI. Este é o primeiro endpoint real do AgendaPro: `POST /sessions`, que recebe uma solicitação de agendamento, valida os dados, chama o caso de uso e retorna o resultado.

## 2. Pré-requisitos
- Plano 001 e Plano 002 concluídos com todos os testes passando ✅
- Variáveis de ambiente configuradas no `.env` (Supabase Dev) ✅

## 3. Fronteiras do Domínio (DDD)
* **Contexto Afetado:** Camada de Entrada (`/src/api/`). Nenhum código em `/src/domain/` ou `/src/infrastructure/` deve ser modificado.
* **Arquivos a serem criados:**
    * `src/api/main.py` — instância do FastAPI e registro dos routers.
    * `src/api/routers/sessions.py` — router com o endpoint `POST /sessions`.
    * `src/api/schemas/session_schemas.py` — schemas Pydantic de Request e Response.
    * `src/api/dependencies.py` — injeção de dependência dos repositórios e use cases via FastAPI `Depends`.

## 4. Arquitetura (Ports & Adapters)
* **Entrada (Port de entrada):** O endpoint HTTP `POST /sessions` é o Adaptador de entrada. Ele recebe JSON, converte para objetos do Domínio e chama o `CreateSessionUseCase`.
* **Saída (Ports de saída):** O `CreateSessionUseCase` já usa os `SessionRepository` e `ProfessorRepository` via injeção de dependência. A API **não deve** chamar repositórios diretamente — apenas Use Cases.
* **Injeção de dependência:** O `dependencies.py` monta o grafo: `SupabaseClient → Repositórios → UseCase`, servido via `Depends` do FastAPI.
* **Schemas Pydantic (Request):**
    ```
    CreateSessionRequest:
      professor_id: UUID
      student_id: UUID
      slot_start: datetime (ISO 8601)
      slot_end: datetime (ISO 8601)
    ```
* **Schemas Pydantic (Response):**
    ```
    SessionResponse:
      id: UUID
      professor_id: UUID
      student_id: UUID
      slot_start: datetime
      slot_end: datetime
      status: str  ("PENDENT_PAYMENT")
      lock_expires_at: datetime
    ```

## 5. Critérios de Aceite e TDD
Os seguintes testes devem ser escritos **antes** da implementação:
1. `tests/unit/api/test_sessions_router.py` — Usando `TestClient` do FastAPI com mocks dos repositórios:
    * Testar `POST /sessions` com dados válidos → deve retornar `201 Created` com `status: PENDENT_PAYMENT`.
    * Testar `POST /sessions` com um slot já ocupado → deve retornar `409 Conflict` com mensagem de erro clara.
    * Testar `POST /sessions` com payload inválido (ex: `slot_end` antes de `slot_start`) → deve retornar `422 Unprocessable Entity`.

## 6. Passos de Implementação (Instrução para a IA Executora)
1. Adicionar dependência `fastapi` e `uvicorn` via `uv add fastapi uvicorn`.
2. Criar `src/api/schemas/session_schemas.py` com os schemas Pydantic.
3. Criar `src/api/dependencies.py` com o grafo de injeção de dependências.
4. **Escrever os testes** em `tests/unit/api/test_sessions_router.py` usando `TestClient` e mocks.
5. Criar `src/api/routers/sessions.py` com o endpoint `POST /sessions`.
6. Criar `src/api/main.py` registrando o router.
7. Rodar `uv run pytest tests/ -v --cov=src` e confirmar que todos os testes (unitários + integração + API) passam.
8. Testar manualmente: `uv run uvicorn src.api.main:app --reload` e acessar `http://localhost:8000/docs` para validar a interface Swagger gerada.
9. Criar o relatório de Hand-off em `/docs/audits/003_01-relatorio_fastapi-camada-entrada.md` e avisar o Humano.
