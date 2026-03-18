# Plano de Execução: 007b - Persistência de Agendamentos (Trilha B)

> 🏗️ **AUTORIA: IA ESTRATÉGICA (ANTIGRAVITY)**
> *Atenção IA Executora (Claude CLI): Este é um micro-plano focado APENAS em infraestrutura. Pare de raciocinar além desse escopo. Leia e execute a Skill associada abaixo.*

## 1. Objetivo do Negócio
Permitir a persistência de aulas (agendamentos) no banco de dados para evitar "double booking". Este plano cuida apenas da ponte entre nosso código e o Supabase.

## 2. Instruções Especiais de Execução
* 🎯 **Skill Demandada:** Você deve obrigatoriamente abrir e ler a regra `/docs/skills/supabase-repository.md` antes de começar.
* ⚠️ **Restrição Geográfica:** NÃO crie a camada FastAPI (rotas). Concentre-se no Repositório (Adapter).

## 3. Arquitetura Exigida
* **Entidade Foco:** `Appointment` (Agendamento).
* **Porta (Interface) Esperada:** `/src/core/ports/appointment_repository.py`
  *(Nota: Se o arquivo da Porta não existir, você tem autorização para criá-lo contendo apenas os métodos exigidos abaixo).*
* **Métodos da Interface/Adapter:**
    - `save(appointment: dict) -> dict`
    - `find_by_time_range(start_time: datetime, end_time: datetime, professor_id: str) -> list`

## 4. O que testar (TDD Oobrigatório)
* O método `save` deve enviar ao Supabase (via chamada apropriada ou mock local testável).
* Se a tentativa de "dar lock" em um horário que já existe (simulada por um erro do banco ao violar unique constrains), expulse a exceção `SlotAlreadyLockedError` dentro do adaptador.

## 5. Fechamento (Passagem do Bastão)
Após implantar a Classe do Adaptador e os Testes, certifique-se que executam localmente. Ao terminar, preencha as etapas descritas na *Condição de Saída* da sua Skill e chame o Diretor (Humano).
