# Plano de Execução: 008a - Regras de Negócio de Agendamento (Trilha A)

> 🏗️ **AUTORIA: IA ESTRATÉGICA (ANTIGRAVITY)**
> *Atenção IA Executora (Claude CLI): Este micro-plano lida estritamente com lógica Pura. Afaste-se de banco de dados neste momento.*

## 1. Objetivo do Negócio
Criar o core lógico que consolida um novo agendamento. Esse Caso de Uso será invocado no futuro pelo Controller do FastAPI quando o Aluno pedir um horário no WhatsApp.

## 2. Instruções Especiais de Execução
* 🎯 **Skill Demandada:** Invoque e siga estritamente `/docs/skills/domain-usecase.md`.
* ⚠️ **Restrição Geográfica:** NÃO crie a camada FastAPI nem adapte o Supabase. Foque em `/src/core/usecases/` e `/tests/unit/core/`.

## 3. Arquitetura Exigida
* **Entidade Foco:** `Appointment` (Agendamento).
* **Portas Injetadas (Dependency Injection):**
    - `IAppointmentRepository` (Para checar conflitos e salvar localmente)
* **Caso de Uso (A ser criado):**
    - `CreateAppointmentUseCase`
* **Método Exigido:**
    - `execute(aluno_id: str, professor_id: str, start_time: datetime, end_time: datetime) -> dict`

## 4. O que testar (TDD Oobrigatório - Mocks Baseados em Memória)
Escreva os seguintes testes unitários usando um FakeRepository simples em memória:
1. `test_create_appointment_success`: Deve falhar se não conseguir criar no cenário ideal.
2. `test_create_appointment_overlap`: Deve lançar o `SlotAlreadyLockedError` doínio se o `find_by_time_range` da interface fake achar um conflito preexistente.
3. `test_invalid_time_range`: Deve lançar erro (ex: `ValidationError`) se `start_time` for maior que `end_time`.

## 5. Fechamento (Passagem do Bastão)
Siga o passo de auditoria prescrito na sua Skill e relate ao Diretor que a tarefa foi concluída.
