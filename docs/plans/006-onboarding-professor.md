# Plano de Execução: 006 - Onboarding do Professor

> 🏗️ **AUTORIA: IA ESTRATÉGICA (ARQUITETO/GEMINI)**
> *Atenção IA Executora (Claude/Cursor): Este plano é a sua única fonte da verdade. Você não tem autoridade para modificar as fronteiras de domínio ou a arquitetura (Ports & Adapters) definida abaixo. A sua única missão é codificar exatamente o que está aqui.*

## 1. Objetivo do Negócio

Permitir que um professor autenticado crie e leia seu próprio perfil de negócio. Hoje o Supabase Auth conhece o professor (UUID), mas a tabela `professors` fica vazia — nenhum endpoint de negócio sabe a qual professor o token pertence. Este plano implementa dois endpoints: `POST /professors/me` (cria perfil) e `GET /professors/me` (lê perfil), ambos protegidos por JWT. O UUID do professor é sempre o `sub` do token — não declarado pelo cliente. Pré-requisito: Planos 001–005 concluídos e ADR 005 aceito.

## 2. Fronteiras do Domínio (DDD)

* **Contexto Afetado:** Módulo de Professores — camadas Domain (apenas erros), Application e API. A Infrastructure (`SupabaseProfessorRepository`) já existe e não precisa de modificação.
* **Entidades/Agregados a serem criados/modificados:**
  - `src/domain/errors.py` (modificar): adicionar `ProfessorAlreadyExistsError` e `ProfessorNotFoundError`
  - `CreateProfessorUseCase` (criar): em `src/application/use_cases/create_professor.py`
  - `GetProfessorUseCase` (criar): em `src/application/use_cases/get_professor.py`

## 3. Arquitetura (Ports & Adapters)

* **Portas (Interfaces necessárias):** Nenhuma nova porta. `ProfessorRepository` já expõe `save(professor)` e `find_by_id(professor_id)` — suficientes para este plano.

* **Adaptadores (Infraestrutura):** `SupabaseProfessorRepository` já implementado no Plano 002. Sem modificações.

* **Casos de Uso (Application Service):**
  - `CreateProfessorUseCase.execute(input) -> Professor`:
    1. Chama `professor_repository.find_by_id(professor_id)` — se encontrado, lança `ProfessorAlreadyExistsError`
    2. Cria entidade `Professor(id=professor_id, name=..., specialty=..., hourly_rate=..., room_link=..., cancellation_tolerance_minutes=...)`
    3. Chama `professor_repository.save(professor)`
    4. Retorna `Professor`
  - `GetProfessorUseCase.execute(professor_id) -> Professor`:
    1. Chama `professor_repository.find_by_id(professor_id)` — se `None`, lança `ProfessorNotFoundError`
    2. Retorna `Professor`

* **Camada de Entrada — Novo router `src/api/routers/professors.py`:**
  - `POST /professors/me` → 201 Created (`ProfessorResponse`) | 409 Conflict (`ProfessorAlreadyExistsError`)
  - `GET /professors/me` → 200 OK (`ProfessorResponse`) | 404 Not Found (`ProfessorNotFoundError`)
  - `professor_id` injetado via `Depends(get_current_professor_id)` em ambos

* **Novos schemas em `src/api/schemas/professor_schemas.py`:**
  - `CreateProfessorRequest`: `name: str`, `specialty: str`, `hourly_rate: Decimal`, `room_link: str`, `cancellation_tolerance_minutes: int`
  - `ProfessorResponse`: todos os campos acima + `id: UUID`

* **`src/api/dependencies.py`:** Adicionar `get_professor_repository`, `get_create_professor_use_case` e `get_get_professor_use_case` seguindo o padrão já estabelecido.

## 4. Critérios de Aceite e TDD

A implementação DEVE passar pelos seguintes testes escritos antes da lógica:

1. `test_create_professor_use_case.py` (novo): professor inexistente → cria e salva com o `professor_id` correto (UUID do JWT)
2. `test_create_professor_use_case.py` (novo): professor já existente → lança `ProfessorAlreadyExistsError`
3. `test_get_professor_use_case.py` (novo): professor existente → retorna `Professor` correto
4. `test_get_professor_use_case.py` (novo): professor inexistente → lança `ProfessorNotFoundError`
5. `test_professors_router.py` (novo): `POST /professors/me` com dados válidos → 201 com `ProfessorResponse`
6. `test_professors_router.py` (novo): `POST /professors/me` com professor já existente → 409 Conflict
7. `test_professors_router.py` (novo): `GET /professors/me` com professor existente → 200 com `ProfessorResponse`
8. `test_professors_router.py` (novo): `GET /professors/me` com professor inexistente → 404 Not Found
9. `test_professors_router.py` (novo): ambos os endpoints sem token → 401

## 5. Passos de Implementação (Instrução para a IA Executora)

1. Adicionar `ProfessorAlreadyExistsError` e `ProfessorNotFoundError` em `src/domain/errors.py`.
2. **Escrever os testes 1 e 2** em `test_create_professor_use_case.py` (Red). Criar `src/application/use_cases/create_professor.py` (Green).
3. **Escrever os testes 3 e 4** em `test_get_professor_use_case.py` (Red). Criar `src/application/use_cases/get_professor.py` (Green).
4. Criar `src/api/schemas/professor_schemas.py` com `CreateProfessorRequest` e `ProfessorResponse`.
5. Adicionar `get_professor_repository`, `get_create_professor_use_case` e `get_get_professor_use_case` em `src/api/dependencies.py`.
6. **Escrever os testes 5 a 9** em `tests/unit/api/test_professors_router.py` (Red). Criar `src/api/routers/professors.py` e registrar em `main.py` (Green).
7. Rodar `uv run pytest tests/unit/ -v --cov=src` e confirmar suite completa passando.
8. Criar relatório de Hand-off em `docs/audits/006_01-relatorio_onboarding-professor.md` e avisar o humano.
