# Plano de Execução: 001 - Configuração Inicial e Domínio Core (Agendamentos e Usuários)

> 🏗️ **AUTORIA: IA ESTRATÉGICA (ARQUITETO/GEMINI)**
> *Atenção IA Executora (Claude/Cursor): Este plano é a sua única fonte da verdade. Você não tem autoridade para modificar as fronteiras de domínio ou a arquitetura (Ports & Adapters) definida abaixo. A sua única missão é codificar exatamente o que está aqui.*

## 1. Objetivo do Negócio
Estabelecer a base fundamental da aplicação `AgendaPro`. O objetivo é criar a estrutura inicial do projeto e implementar o Domínio Core: os modelos limpos que representam um Professor, um Aluno e uma Sessão (Agendamento avulso com lock temporário), sem ainda conectá-los a bancos de dados ou APIs externas.

## 2. Fronteiras do Domínio (DDD)
* **Contexto Afetado:** Módulo de Agendamentos / Módulo de Usuários.
* **Entidades/Agregados a serem criados:**
    * `Professor`: Entidade contendo dados do onboarding (Especialidade, valor da hora, link da sala, tolerância).
    * `Student` (Aluno): Entidade contendo os dados de contato, principal deles o WhatsApp (identificador único para a IA).
    * `Session` (Sessão/Agendamento): O agregado principal. Contém referência do professor, do aluno, o `slot` de tempo, o status do pagamento (Pendente/Confirmado/Cancelado) e, crucialmente, o campo auxiliar para o `lock` de 10 minutos pré-pagamento.

## 3. Arquitetura (Ports & Adapters)
* **Portas (Interfaces necessárias):**
    * `ProfessorRepository`: Para salvar/buscar preferências do professor.
    * `StudentRepository`: Para gerenciar os perfis dos alunos que interagem.
    * `SessionRepository`: Para criar agendamentos e gerenciar as consultas livres e travadas pelo lock.
* **Adaptadores (Infraestrutura):** Nenhum neste passo. Faremos o deploy da lógica pura (em memória) ou com mocks para garantir o isolamento.
* **Casos de Uso (Application Service):**
    * `CreateSessionUseCase`: Lida com a tentativa de criar um agendamento novo, garantindo que o slot está livre, aplicando o lock e deixando com status "Pendente" aguardando o link de pagamento.

## 4. Critérios de Aceite e TDD
A implementação DEVE passar pelos seguintes testes que devem ser escritos primeiro:
1. **[CreateSessionUseCase]** Teste unitário verificando se não é possível agendar uma `Session` em um horário já ocupado (lançar `SlotAlreadyBookedError`).
2. **[CreateSessionUseCase]** Teste unitário garantindo que a `Session` recém-criada inicia obrigatoriamente no status `PENDENT_PAYMENT` e contém as datas de expiração do lock (agora + 10 min).

## 5. Passos de Implementação (Instrução para a IA Executora)
1. Iniciar a estrutura de pastas do código fonte (ex: `/src/domain`, `/src/application`, `/src/infrastructure`, `/tests`).
2. Escrever os Testes Unitários das Entidades (`Professor`, `Student` e `Session`) validando as regras de estado/status.
3. Implementar as Entidades (Domain).
4. Escrever as Interfaces de Repositório (Ports) no pacote `/src/domain/ports/`.
5. Escrever os Testes Unitários do `CreateSessionUseCase` com mocks dos repositórios.
6. Implementar a lógica do `CreateSessionUseCase` (em `/src/application/use_cases/`).
7. Rodar a esteira de testes com Pytest evidenciando 100% de cobertura neste escopo.
