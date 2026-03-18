# Plano de Execução: 004 - Autenticação JWT com Supabase Auth

> 🏗️ **AUTORIA: IA ESTRATÉGICA (ARQUITETO/GEMINI)**
> *Atenção IA Executora (Claude/Cursor): Este plano é a sua única fonte da verdade. Você não tem autoridade para modificar as fronteiras de domínio ou a arquitetura (Ports & Adapters) definida abaixo. A sua única missão é codificar exatamente o que está aqui.*

## 1. Objetivo do Negócio

Proteger o endpoint `POST /sessions` com autenticação JWT baseada no Supabase Auth. Atualmente, qualquer cliente anônimo pode criar sessões para qualquer professor — isso é uma falha crítica de segurança (dívida técnica #1 do Plano 003). Após este plano, somente um professor autenticado poderá criar sessões e apenas **para si próprio** (o `professor_id` será extraído do token JWT, nunca do body da requisição).

## 2. Pré-requisitos

- Plano 001, 002 e 003 concluídos ✅
- Variável de ambiente `SUPABASE_JWT_SECRET` disponível no `.env` (obter em: Supabase Dashboard → Project Settings → API → JWT Secret)

## 3. Fronteiras do Domínio (DDD)

- **Contexto Afetado:** Exclusivamente `src/api/` (Camada de Entrada).
- **PROIBIDO:** Qualquer modificação em `src/domain/` ou `src/infrastructure/`.
- A autenticação é responsabilidade do Adaptador de Entrada. O Domínio e a Infraestrutura permanecem cegos a JWT.

## 4. Arquitetura (Ports & Adapters)

### Novo arquivo: `src/api/auth.py`
Responsável exclusivamente pela validação do JWT. Deve expor uma única função de dependência do FastAPI:

```python
def get_current_professor_id(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())]
) -> UUID:
    ...
```

**Lógica de validação:**
1. Extrair o token do header `Authorization: Bearer <token>`.
2. Decodificar o JWT usando `PyJWT` com o `SUPABASE_JWT_SECRET` do ambiente e algoritmo `HS256`.
3. Validar que `payload["role"] == "authenticated"`.
4. Retornar `UUID(payload["sub"])` como `professor_id`.
5. Lançar `HTTPException(status_code=401)` se o token for inválido, expirado ou ausente.
6. Lançar `HTTPException(status_code=403)` se `role != "authenticated"`.

### Modificação: `src/api/schemas/session_schemas.py`
- **Remover** o campo `professor_id: UUID` de `CreateSessionRequest`.
- `professor_id` agora virá **exclusivamente** do JWT. Qualquer cliente que enviar `professor_id` no body deve receber um payload limpo (o campo extra é ignorado pelo Pydantic por padrão).

### Modificação: `src/api/routers/sessions.py`
- Adicionar `professor_id: Annotated[UUID, Depends(get_current_professor_id)]` como parâmetro do endpoint.
- Usar este `professor_id` do JWT ao construir o `CreateSessionInput`.
- Remover a leitura de `body.professor_id`.

### Modificação: `src/api/dependencies.py`
- Adicionar `get_professor_repository` para suportar lookups futuros (não obrigatório neste plano, mas preparar a fábrica seguindo o padrão já estabelecido).

### Nova variável de ambiente

Adicionar ao `.env` (e ao `.env.example` se existir):
```
SUPABASE_JWT_SECRET=seu-jwt-secret-aqui
```

## 5. Critérios de Aceite e TDD

Os seguintes testes devem ser escritos **antes** da implementação (TDD):

**Arquivo: `tests/unit/api/test_auth.py`** (NOVO)
1. Token JWT válido + role `authenticated` → retorna `UUID` correto do campo `sub`.
2. Token JWT expirado → lança `HTTPException(401)`.
3. Token JWT com assinatura inválida → lança `HTTPException(401)`.
4. Token JWT com `role != "authenticated"` (ex: `"anon"`) → lança `HTTPException(403)`.
5. Header `Authorization` ausente → FastAPI retorna `403` automaticamente via `HTTPBearer`.

**Arquivo: `tests/unit/api/test_sessions_router.py`** (MODIFICAR)

Os 4 testes existentes devem ser adaptados:
- Remover `professor_id` do payload enviado no body.
- Adicionar o mock da dependência `get_current_professor_id` (retornando um UUID fixo) via `dependency_overrides`.
- O `professor_id` esperado no response deve ser o mesmo retornado pelo mock de auth.

**Novos testes a adicionar no arquivo modificado:**
6. `POST /sessions` sem header `Authorization` → retorna `403`.
7. `POST /sessions` com token inválido (mock de `get_current_professor_id` lançando `HTTPException(401)`) → retorna `401`.

## 6. Passos de Implementação (Instrução para a IA Executora)

1. Instalar dependência: `uv add pyjwt`.
2. Adicionar `SUPABASE_JWT_SECRET` ao `.env` (solicitar o valor ao humano se não estiver disponível).
3. **Escrever os 5 testes unitários** em `tests/unit/api/test_auth.py` — eles devem falhar (Red).
4. Criar `src/api/auth.py` com a função `get_current_professor_id` — fazê-los passar (Green).
5. Refatorar `src/api/schemas/session_schemas.py`: remover `professor_id` de `CreateSessionRequest`.
6. Refatorar `src/api/routers/sessions.py`: usar `professor_id` do JWT.
7. **Atualizar os testes existentes** em `tests/unit/api/test_sessions_router.py`: adaptar os 4 testes existentes e adicionar os 2 novos testes de auth.
8. Rodar `uv run pytest tests/ -v --cov=src` e confirmar suite completa passando (mínimo 36 testes).
9. Criar ADR 003 em `docs/adr/003-autenticacao-jwt-supabase.md` documentando a decisão.
10. Criar o relatório de Hand-off em `docs/audits/004_01-relatorio_autenticacao-jwt.md`.
11. Avisar o humano que terminou e pedir para enviar o relatório ao Arquiteto.

> ⚠️ **ATENÇÃO:** O campo `professor_id` sendo removido do body é uma mudança que quebra a API pública. Isso é intencional. A nova contrato é: professores autenticados não precisam (e não devem) informar seu próprio ID no body.
