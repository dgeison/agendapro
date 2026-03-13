# Plano de Execução: 002 - Infraestrutura de Persistência (Supabase)

> 🏗️ **AUTORIA: IA ESTRATÉGICA (ARQUITETO/GEMINI)**
> *Atenção IA Executora (Claude/Cursor): Este plano é a sua única fonte da verdade. Você não tem autoridade para modificar as fronteiras de domínio ou a arquitetura (Ports & Adapters) definida abaixo. A sua única missão é codificar exatamente o que está aqui.*

## 1. Objetivo do Negócio
Conectar o Domínio Core existente (Plano 001) ao banco de dados real. Implementar os Adaptadores concretos de infraestrutura que conectam as Portas (`ProfessorRepository`, `StudentRepository`, `SessionRepository`) ao Supabase (PostgreSQL), usando o ambiente `agendapro-dev`.

## 2. Pré-requisitos (Checklist do Humano)
Antes de acionar a IA Executora, o Humano deve:
- [ ] Criar um projeto chamado `agendapro-dev` no Supabase (supabase.com).
- [ ] Copiar a `SUPABASE_URL` e a `SUPABASE_SERVICE_ROLE_KEY` do projeto recém-criado.
- [ ] Criar um arquivo `.env` na raiz do projeto `agendapro` com o seguinte conteúdo:
```
SUPABASE_URL=https://<seu-id>.supabase.co
SUPABASE_KEY=<sua-service-role-key>
DATABASE_URL=postgresql://postgres:<sua-senha>@db.<seu-id>.supabase.co:5432/postgres
```
- [ ] Adicionar `.env` ao `.gitignore` (se ainda não estiver).

## 3. Fronteiras do Domínio (DDD)
* **Contexto Afetado:** Módulo de Infraestrutura. **Nenhuma** entidade de Domínio existente deve ser modificada.
* **Arquivos a serem criados (apenas em `/src/infrastructure/`):**
    * `SupabaseProfessorRepository` (implementação de `ProfessorRepository`)
    * `SupabaseStudentRepository` (implementação de `StudentRepository`)
    * `SupabaseSessionRepository` (implementação de `SessionRepository`)
    * `database.py` (cliente Supabase singleton configurado via `.env`)

## 4. Arquitetura (Ports & Adapters)
* **Portas (Interfaces):** Já existem em `/src/domain/ports/`. **Não altere.**
* **Adaptadores (a criar):** Em `/src/infrastructure/repositories/`, criar os três repositórios concretos usando a biblioteca `supabase-py`.
* **Migrations (Schema do Banco):** Criar os scripts SQL para as tabelas `professors`, `students` e `sessions` em `/src/infrastructure/migrations/`. A tabela `sessions` deve conter obrigatoriamente os campos `status` (ENUM: `PENDENT_PAYMENT`, `CONFIRMED`, `CANCELLED`) e `lock_expires_at` (TIMESTAMP).

## 5. Critérios de Aceite e TDD
Os seguintes testes de integração devem ser escritos e executados **contra o banco `agendapro-dev`**:
1. `test_supabase_session_repository.py`: Testar que `create()` salva uma `Session` com status `PENDENT_PAYMENT` e `lock_expires_at` preenchido.
2. `test_supabase_session_repository.py`: Testar que `find_by_slot()` retorna a sessão correta ao buscar por professor e intervalo de tempo.
3. `test_supabase_professor_repository.py`: Testar que `save()` persiste um `Professor` e que `find_by_id()` o recupera com os dados corretos.

## 6. Passos de Implementação (Instrução para a IA Executora)
1. Adicionar a dependência `supabase` ao projeto via `uv add supabase`.
2. Criar `/src/infrastructure/database.py` com o cliente Supabase lendo as variáveis do `.env` com `python-dotenv`.
3. Criar os scripts de migration SQL em `/src/infrastructure/migrations/001_create_tables.sql`.
4. Criar os três Adaptadores de Repositório em `/src/infrastructure/repositories/`.
5. Escrever os testes de integração em `/tests/integration/`.
6. Rodar `uv run pytest tests/integration/ -v` para validar.
7. Ao finalizar, criar o relatório de Hand-off em `/docs/audits/002-relatorio.md` com o resultado dos testes e a cobertura total.
8. Avisar o Humano que terminou e pedir para ele enviar o relatório ao Arquiteto.
