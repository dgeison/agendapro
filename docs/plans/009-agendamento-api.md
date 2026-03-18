# Plano de Execução: 009 - Injeção e Endpoint de Agendamentos (Trilha A)

> 🏗️ **AUTORIA: IA ESTRATÉGICA (ANTIGRAVITY) - FASE DE FAN-IN**
> *Atenção IA Executora: Esse é um plano de Integração Final (Fan-In). Nossas Trilhas Paralelas anteriores já criaram o Banco de Dados (Adapters) e a Regra Pura Lógica (Use Case). Sua missão é conectar tudo através de uma Rota Web (FastAPI).*

## 1. Objetivo do Negócio
Expor um endpoint `/appointments` de método `POST` para que sistemas externos (ex: a futura integração com Meta/WhatsApp) possam criar agendamentos e iniciar o Lock da Agenda.

## 2. Instruções Especiais de Execução
* 🎯 **Skill Demandada:** `/docs/skills/fastapi-endpoint.md`
* ⚠️ **Restrição Geográfica:** Não modifique os testes de Repositório (`/tests/integration/infra`) nem testes do Core. Altere APENAS `/src/api` e `/tests/integration/api`.

## 3. Arquitetura Exigida (A Ponte)
* **Rota HTTP a Criar:** `@router.post("/appointments", response_model=AppointmentResponse, status_code=201)` no arquivo apropriado (ex: `src/api/routes/appointments_router.py`).
* **Input Pydantic:** `AppointmentCreateRequest` contendo `aluno_id`, `start_time` e `end_time` (assumimos que o `professor_id` pode vir do JWT no futuro, mas por enquanto exija no input/dependência caso não tenha auth finalizada ali).
* **Mapeamento (A Injeção de Dependências):** 
    - O Endpoint precisa da dependência FastAPI (ex: função `ProvidesUseCase()`) que saiba instanciar o `SupabaseAppointmentRepository()` e e injetá-lo no `CreateAppointmentUseCase()`.

## 4. O que testar (TestClient)
* `test_post_appointments_success`: Retorna HTTP 201 (Created) validando contrato JSON.
* `test_post_appointments_overlap_conflict`: Provoca a exceção do domínio e verifica se o Endpoint lida retornando um limpo erro HTTP 409 (Conflict), evitando o vazamento cego de exceções com erro 500 do FastAPI.
* `test_post_appointments_invalid_schema`: Provoca erros de payload JSON confirmando HTTP 422 da lib Pydantic.

## 5. Fechamento
Ao atingir Cobertura Verde, declare concluído e desça do terminal.
