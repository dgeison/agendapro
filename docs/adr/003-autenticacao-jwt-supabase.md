# ADR 003: Autenticação JWT via Supabase Auth na Camada de Entrada
**Data:** 2026-03-13 | **Status:** Aceito

## Contexto

O endpoint `POST /sessions` era público: qualquer cliente anônimo podia criar sessões para qualquer professor, passando `professor_id` livremente no body. Isso constituía a dívida técnica #1 (Alta) do Plano 003. Era necessário garantir que somente professores autenticados criem sessões e que o `professor_id` seja sempre derivado do token assinado — nunca declarado pelo cliente.

## Decisão

A autenticação JWT é responsabilidade exclusiva da Camada de Entrada (`src/api/`). Uma dependência FastAPI (`get_current_professor_id` em `src/api/auth.py`) valida o Bearer token emitido pelo Supabase Auth usando `PyJWT` com algoritmo `HS256` e segredo `SUPABASE_JWT_SECRET`. O `professor_id` é extraído do campo `sub` do token e injetado via `Depends()`. O campo `professor_id` foi removido de `CreateSessionRequest`. O Domínio e a Infraestrutura permanecem 100% cegos ao JWT. Token ausente ou inválido retorna `401` (conforme RFC 7235); role diferente de `authenticated` retorna `403`.

## Consequências

* **Positivas:** Impersonation impossível — `professor_id` vem sempre do token assinado pelo Supabase. Domínio isolado de detalhes de autenticação (Arquitetura Hexagonal preservada). Contrato da API simplificado: cliente não declara nem consegue forjar seu próprio ID.
* **Negativas:** Breaking change na API: clientes que enviavam `professor_id` no body precisam ser atualizados. `SUPABASE_JWT_SECRET` deve ser provisionado manualmente em cada ambiente (dev e prod).
