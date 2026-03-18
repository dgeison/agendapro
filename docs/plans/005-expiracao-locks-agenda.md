# Plano de Execução: 005 - Expiração de Locks de Agenda

> 🏗️ **AUTORIA: IA ESTRATÉGICA (ARQUITETO/GEMINI)**
> *Atenção IA Executora (Claude/Cursor): Este plano é a sua única fonte da verdade. Você não tem autoridade para modificar as fronteiras de domínio ou a arquitetura (Ports & Adapters) definida abaixo. A sua única missão é codificar exatamente o que está aqui.*

## 1. Objetivo do Negócio

O PRD define que um slot bloqueado deve ser liberado automaticamente se o pagamento não for confirmado em 10 minutos. Atualmente, sessões `PENDENT_PAYMENT` com `lock_expires_at` vencido ficam bloqueadas para sempre — inviabilizando reuse do slot. Este plano implementa o mecanismo de expiração automática: um job periódico detecta e expira esses locks, tornando os slots disponíveis novamente sem intervenção humana. Pré-requisito: Planos 001–004 concluídos e ADR 004 aceito.

## 2. Fronteiras do Domínio (DDD)

* **Contexto Afetado:** Módulo de Agendamentos — camadas Domain, Application, Infrastructure e API (nesta ordem de dependência).
* **Entidades/Agregados a serem criados/modificados:**
  - `Session` (modificar): adicionar `SessionStatus.EXPIRED` e método `session.expire()`
  - `ExpireSessionLocksUseCase` (criar): caso de uso de expiração em lote em `src/application/use_cases/`

## 3. Arquitetura (Ports & Adapters)

* **Portas (Interfaces necessárias):** Adicionar dois métodos à interface `SessionRepository` em `src/domain/ports/session_repository.py`:
  - `find_expired_pending() -> list[Session]`: retorna sessões com `status=PENDENT_PAYMENT` e `lock_expires_at < now()`
  - `update_status(session: Session) -> None`: persiste mudança de status

* **Adaptadores (Infraestrutura):** Implementar os dois novos métodos em `SupabaseSessionRepository` (`src/infrastructure/repositories/supabase_session_repository.py`):
  - `find_expired_pending`: `SELECT * FROM sessions WHERE status = 'PENDENT_PAYMENT' AND lock_expires_at < now()`
  - `update_status`: `UPDATE sessions SET status = :status WHERE id = :id`

* **Casos de Uso (Application Service):** `ExpireSessionLocksUseCase.execute() -> int`:
  1. Chama `session_repository.find_expired_pending()`
  2. Para cada sessão: chama `session.expire()`
  3. Chama `session_repository.update_status(session)`
  4. Retorna contagem de sessões expiradas (para observabilidade)

* **Camada de Entrada — Task Periódica:** Adicionar `lifespan` em `src/api/main.py` com `asyncio.create_task` que executa `ExpireSessionLocksUseCase` a cada `LOCK_EXPIRY_INTERVAL_SECONDS` segundos (padrão: 60). O loop deve logar a contagem quando `expired_count > 0`. Adicionar `LOCK_EXPIRY_INTERVAL_SECONDS=60` ao `.env`.

## 4. Critérios de Aceite e TDD

A implementação DEVE passar pelos seguintes testes escritos antes da lógica:

1. `test_session.py` (modificar): `session.expire()` em sessão `PENDENT_PAYMENT` com lock vencido → `status == EXPIRED`
2. `test_session.py` (modificar): `session.expire()` em sessão já `EXPIRED` → lança `ValueError`
3. `test_session.py` (modificar): `session.expire()` com lock ainda vigente → lança `ValueError`
4. `test_expire_session_locks_use_case.py` (novo): 2 sessões expiradas → `update_status` chamado 2x, retorna `2`
5. `test_expire_session_locks_use_case.py` (novo): sem sessões expiradas → retorna `0`, `update_status` não chamado
6. `test_main.py` (novo): task de background cancela sem leak ao receber `CancelledError`
7. `test_supabase_session_repository.py` (integração, modificar): `find_expired_pending()` retorna apenas sessões vencidas
8. `test_supabase_session_repository.py` (integração, modificar): `update_status()` persiste mudança no banco

## 5. Passos de Implementação (Instrução para a IA Executora)

1. Adicionar `EXPIRED` ao `SessionStatus` e método `expire()` em `src/domain/entities/session.py` — escrever os testes 1, 2 e 3 antes (Red), depois implementar (Green).
2. Adicionar `find_expired_pending` e `update_status` à interface `src/domain/ports/session_repository.py`.
3. Criar `src/application/use_cases/expire_session_locks.py` — escrever os testes 4 e 5 antes (Red), depois implementar (Green).
4. Implementar `find_expired_pending` e `update_status` em `SupabaseSessionRepository`.
5. Escrever os testes de integração 7 e 8.
6. Adicionar `lifespan` e `_run_lock_expiry_loop` em `src/api/main.py`. Escrever o teste 6.
7. Adicionar `LOCK_EXPIRY_INTERVAL_SECONDS=60` ao `.env`.
8. Rodar `uv run pytest tests/unit/ -v --cov=src` e confirmar suite completa passando.
9. Criar relatório de Hand-off em `docs/audits/005_01-relatorio_expiracao-locks.md` e avisar o humano.
