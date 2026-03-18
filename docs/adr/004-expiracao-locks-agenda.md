# ADR 004: Estratégia de Expiração de Locks de Agenda
**Data:** 2026-03-13 | **Status:** Aceito

## Contexto

O Domínio cria sessões com `status=PENDENT_PAYMENT` e `lock_expires_at = now() + 10min`. Se o pagamento não for confirmado, o slot deve ser liberado automaticamente conforme o PRD. Sem isso, slots ficam bloqueados indefinidamente, tornando o agendamento inviável. É necessário um mecanismo periódico que detecte e expire esses locks. Três alternativas foram avaliadas: (A) pg_cron no Supabase — viola DDD ao colocar lógica de negócio no banco, e não disponível no tier gratuito; (B) Celery + Redis — robusto, mas adiciona Redis desnecessariamente ao MVP; (C) asyncio + lifespan do FastAPI — zero dependências novas, mantém DDD, testável.

## Decisão

Usar task periódica com `asyncio.create_task` no `lifespan` do FastAPI (Opção C). A lógica de expiração vive em `ExpireSessionLocksUseCase` no Domínio, respeitando a Arquitetura Hexagonal. O banco é acessado via o `SessionRepository` existente. O intervalo é configurável via variável de ambiente `LOCK_EXPIRY_INTERVAL_SECONDS` (padrão: 60 segundos).

## Consequências

* **Positivas:** Zero dependências externas novas. Lógica de expiração no Domínio (DDD correto). Testável via mock do repositório. Intervalo configurável por ambiente.
* **Negativas:** Jobs não persistem entre reinicializações do processo — aceitável para o MVP (sessões expiradas são detectadas e tratadas na próxima execução do loop). Para produção com múltiplas instâncias, migrar para Celery.
