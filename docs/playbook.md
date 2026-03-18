# 📘 PLAYBOOK DE DESENVOLVIMENTO SOLO COM IA

> **Status:** Ativo | **Última Atualização:** 2026-03-12 | **Versão:** 1.1.0
> *Este documento é versionado como software. Sempre que um gargalo operacional ocorrer, o processo será re-arquitetado e a versão documentada abaixo.*

### Histórico de Rastreamento (Changelog)
| Versão | Data | Alteração | Motivo/Conflito Resolvido |
| :--- | :--- | :--- | :--- |
| **v1.1.0** | 2026-03-12 | Injeção do bloco `⚠️ IDENTIDADE E LIMITES DE MÁQUINA` no `.clauderules` e `🏗️ AUTORIA: IA ESTRATÉGICA` no Artefato B. | Conflito: Ambiguidade de responsabilidade; IA Executora (Claude) não pode ter margem para alterar arquitetura sem permissão. |
| **v1.0.0** | 2026-03-12 | Criação inicial do Playbook (Mandamentos, Regra de WIP, Motor de Contexto e Artefatos). | Formalizar o processo de engenharia ponta a ponta com IA. |

---

**O Sistema Operacional do Engenheiro de Software**

## 1. O Paradigma e Papéis

A Inteligência Artificial não substitui o engenheiro; ela substitui a digitação. Para que o desenvolvimento seja previsível e escalável, a separação de papéis é inegociável:

* **Humano (Diretor/PM):** Define *o que* deve ser feito, gerencia o estado das tarefas (no tracker) e aprova o código final (CI/CD). Nunca escreve lógica de negócios manualmente.
* **IA Estratégica (Arquiteto - Ex: Gemini):** Pensa. Recebe o problema do humano, audita logs, analisa riscos e gera os Planos de Execução (`/docs/plans`) e as Decisões de Arquitetura (`/docs/adr`).
* **IA Executora (Operário - Ex: Claude/Cursor):** Digita. Lê os planos gerados pelo Arquiteto e traduz para código. **A IA Executora é estritamente proibida de tomar decisões arquiteturais.**

## 2. Os 4 Mandamentos Arquiteturais

Qualquer código gerado pela IA Executora deve obrigatoriamente respeitar estes quatro pilares. Se quebrar um deles, o código é rejeitado.

1. **Domain-Driven Design (DDD):** O sistema é dividido em Contextos Delimitados (Bounded Contexts). A IA só recebe o contexto da feature atual para evitar contaminação cruzada. A linguagem ubíqua deve ser mantida (o nome no banco de dados, no código e na tarefa devem ser idênticos).
2. **Arquitetura Hexagonal (Ports & Adapters):** O Domínio (Core) não sabe que a internet ou o banco de dados existem. Toda comunicação com o mundo externo (banco de dados, APIs, filas de mensageria) deve ser feita através de Portas (Interfaces). A IA deve sempre implementar Adaptadores isolados para conectar as Portas à infraestrutura.
3. **Test-Driven Development (TDD):** A IA Executora deve **sempre** escrever os testes (unitários e de integração) *antes* da lógica de negócios. O fluxo inegociável é: escrever o teste que falha (Red), implementar a lógica da feature (Green) e otimizar (Refactor).
4. **Clean Code:** Funções devem ter responsabilidade única. A injeção de dependência é obrigatória. Classes e arquivos não devem se tornar monolíticos. O código deve ser legível para humanos.

## 3. O Ecossistema e a Regra do WIP

* **Estado (Linear/Plane):** Onde os tickets vivem.
* **Conhecimento (Obsidian/Markdown):** Onde as decisões e planos vivem.
* **WIP Limit (Work in Progress) = 1:** O humano e a IA Executora só trabalham em **uma** feature por vez. Jamais misture refatoração com criação de feature no mesmo ciclo de prompt.

## 4. A Estrutura de Diretórios (O Motor de Contexto)

O repositório do projeto conterá uma pasta `/docs` que serve como o cérebro do projeto.

* `/docs/adr/` *(Architecture Decision Records)*: Leis imutáveis. O "por que" escolhemos um banco específico, um padrão de concorrência ou uma biblioteca. A IA Executora lê para não violar o passado.
* `/docs/audits/`: Relatórios de Hand-off (passagem de bastão). Sempre que a IA Executora terminar um plano, ela deve gerar aqui um relatório do que foi feito para a IA Estratégica (Arquiteto) validar. **Convenção de nomenclatura:** `{plano}_{iteração}-relatorio_{descrição}.md`. Exemplo: `002_02-relatorio_infraestrutura-supabase-concluido.md`. Um mesmo plano pode gerar múltiplas iterações de relatório (bloqueio, retentativa, conclusão).
* `/docs/plans/`: Os Planos de Execução. O mapa exato do que a IA Executora deve codar no ciclo atual.

---

## 5. Artefatos Operacionais (Templates)

### Artefato A: O `.clauderules` (A Constituição da IA Executora)

*Salve este conteúdo na raiz do repositório como `.clauderules` (Instruções lidas pelo Claude CLI).*

```markdown
# ⚠️ IDENTIDADE E LIMITES DE MÁQUINA (SYSTEM RULES)

**VOCÊ É A IA EXECUTORA (O OPERÁRIO).**
*   **A sua responsabilidade:** Escrever código, criar testes, configurar arquivos e implementar a lógica braçal com perfeição técnica.
*   **A DELE (Gemini/Arquiteto):** Pensar, desenhar a arquitetura geral, escolher as tecnologias e redigir os planos na pasta `/docs/plans/`.
*   **O LIMITE:** Você é ESTRITAMENTE PROIBIDA de tomar decisões arquiteturais, alterar o escopo ou inventar padrões não documentados. Se o plano escrito pelo Arquiteto contiver um erro que impeça o desenvolvimento, **NÃO INVENTE UMA SOLUÇÃO**. Pare imediatamente e notifique o Humano para que o Arquiteto corrija o plano.

## REGRAS INEGOCIÁVEIS:
1. **Zero Alucinação Arquitetural:** Nunca inicie o desenvolvimento de uma feature sem ler o arquivo correspondente em `/docs/plans/`.
2. **Histórico:** Antes de alterar configurações de infraestrutura, I/O, bancos de dados ou serviços externos, leia os arquivos em `/docs/adr/` para não violar as decisões arquiteturais passadas.
3. **Arquitetura Hexagonal:** Mantenha o Core (Domínio) 100% isolado. Dependências externas (APIs, DBs, Kafka, etc.) devem ser implementadas através de Interfaces (Ports) e injetadas (Adapters).
4. **TDD e Bloqueio de Retries:** Você DEVE escrever os testes unitários e/ou de integração antes de implementar a regra de negócios. Siga o ciclo Red-Green-Refactor. **Se um teste falhar por 3 tentativas consecutivas, PARE**, documente o erro e chame o humano.
5. **Clean Code e Observabilidade:** Use injeção de dependência e funções curtas. Erros devem gerar logs estruturados (JSON) ricos em contexto; nunca silencie erros inadvertidamente.
6. **Hand-off (Passagem de Bastão):** Quando você terminar de implementar um Plano de Execução, **você também é responsável por rodar os testes** (`pytest`) e confirmar que passam. Só então crie um arquivo markdown em `/docs/audits/` com o resumo do que foi implementado, a cobertura de testes e quaisquer dívidas técnicas. Em seguida, avise o humano que terminou e peça para ele enviar este relatório ao Arquiteto. **NÃO PARE EM SILÊNCIO.**

```

### Artefato B: Template do Plano de Execução (`/docs/plans/TEMPLATE.md`)

*O Arquiteto (Gemini) preencherá este arquivo para o Operário (Claude) executar.*

```markdown
# Plano de Execução: [Nome da Feature/Ticket]

> 🏗️ **AUTORIA: IA ESTRATÉGICA (ARQUITETO/GEMINI)**
> *Atenção IA Executora (Claude/Cursor): Este plano é a sua única fonte da verdade. Você não tem autoridade para modificar essas fronteiras de domínio ou a arquitetura (Ports & Adapters) definida abaixo. A sua única missão é codificar exatamente o que está aqui.*

## 1. Objetivo do Negócio
[Descrição concisa do que precisa ser alcançado]

## 2. Fronteiras do Domínio (DDD)
* **Contexto Afetado:** [Ex: Módulo de Agendamentos / Módulo de Pagamentos]
* **Entidades/Agregados a serem criados/modificados:** [Nomes exatos]

## 3. Arquitetura (Ports & Adapters)
* **Portas (Interfaces necessárias):** [Ex: UserRepository interface]
* **Adaptadores (Infraestrutura):** [Ex: Implementação do PostgresUserRepository usando GORM ou SQLAlchemy]
* **Casos de Uso (Application Service):** [Ex: CreateUserUseCase]

## 4. Critérios de Aceite e TDD
A implementação DEVE passar pelos seguintes testes que devem ser escritos primeiro:
1. [Ex: Teste unitário verificando se o erro 'UserAlreadyExists' é lançado]
2. [Ex: Teste de integração garantindo que o adaptador salva no banco]

## 5. Passos de Implementação (Instrução para a IA Executora)
1. Escrever as Interfaces (Ports).
2. Escrever os Testes Unitários dos Casos de Uso.
3. Implementar os Casos de Uso (Domain).
4. Escrever o Adaptador de Infraestrutura e seus testes.
5. Fazer a injeção de dependência na camada de entrada (Controller/Handler).

```

### Artefato C: Template de ADR (`/docs/adr/TEMPLATE.md`)

```markdown
# ADR [Número]: [Título Curto da Decisão]
**Data:** [YYYY-MM-DD] | **Status:** [Proposto / Aceito / Obsoleto]

## Contexto
[Qual é a força motriz, o problema técnico ou o gargalo que exige uma decisão arquitetural?]

## Decisão
[A escolha técnica exata. Ex: "Vamos usar UUID v7 como chaves primárias em todos os novos modelos de banco de dados em vez de inteiros seriais."]

## Consequências
* **Positivas:** [Ex: Escalabilidade global, evita colisão em concorrência].
* **Negativas:** [Ex: Maior uso de armazenamento no banco de dados].

```

---

## 6. Fluxo de Trabalho e Guardrails (Regras Operacionais)

Para que essa engrenagem rode em um ambiente de produção real sem engessar a equipe ou deixar portas abertas para código quebrado, siga estes guardrails:

1. **Versionamento e Branches (Trunk-Based):** Crie branches de curta duração para cada Plano de Execução (ex: `feat/001-agendamento`). O merge para a branch principal só ocorre por via de Pull Request analisado pelo Humano e aprovado pelo CI.
2. **Integração Contínua (CI/CD):** O CI é a sua barreira final de qualidade. A esteira deve rodar *Linters rigorosos* e os testes automatizados criados pela IA. Se o CI quebrar, a IA Executora recebe os logs para correção.
3. **A Exceção "Spike" (Prova de Conceito):** TDD rígido pode atrapalhar a fase de descoberta experimental. Se você não sabe se uma biblioteca ou API resolve o seu problema, isole-se em um código de "Spike" (código focado em provar um conceito rapidamente, descartando regras). Validada a ideia científica, aquilo deve gerar um ADR, o código sujo **é descartado**, e a IA então reconstrói no projeto principal seguindo as regras e o TDD.

## 7. O Ponto de Partida (Como "Dar o Start")

Antes de escrever qualquer lógica de sistema, você (Diretor) e a IA Estratégica (Arquiteto) devem executar o **Kickoff do Projeto**:

1. **Criar a Fundação:** Inicialize o repositório principal e crie as pastas base do Motor de Contexto: `/docs/adr`, `/docs/plans` e `/docs/audits`.
2. **Aprovar a Constituição:** Salve o conteúdo do "Artefato A" na raiz do repositório como o arquivo `.clauderules`. Isso baliza de imediato o Claude CLI.
3. **Criar o Marco Zero (ADR-001):** Crie um ADR definindo a fundação técnica inegociável do projeto (ex: Backend de APIs com FastAPI, Persistência com Supabase PostgreSQL).
4. **Construir o Sentinela:** Faça o setup básico de uma pipeline CI contendo apenas Linter e runner de Testes da linguagem que você escolheu.
5. **Planejar o Primeiro Passo:** Entregue o seu Documento de Requisitos do Produto (PRD) para a IA Estratégica e peça: *“Crie o plano de execução `/docs/plans/001-setup-dominio.md` focado em construir as Entidades Fundamentais e a estrutura física do Clean Architecture”*.

---

## 8. Protocolo de Troca de Modelo ou Sessão (Anti-Amnesia)

Modelos de IA não têm memória entre sessões. O contexto que existe em uma janela de chat **desaparece** ao ser fechada. Para nunca perder o estado do projeto, siga este protocolo:

**Regra de Ouro:** A memória do projeto vive no repositório, não na janela de chat.

**Ao abrir uma nova sessão com a IA Estratégica (Arquiteto/Gemini):**
1. Envie o arquivo `/docs/audits/` mais recente gerado pela IA Executora (o Hand-off do último ciclo).
2. Envie o `ADR` mais recente, se houver um criado recentemente.
3. Descreva em uma linha: *"Acabamos de concluir o Plano [N]. Nosso próximo objetivo é [X]."*

**Ao abrir uma nova sessão com a IA Executora (Operário/Claude/Cursor/Windsurf):**
1. Abra o terminal na pasta do projeto. O Claude CLI será alimentado pelo nosso `.clauderules` e outros pontos de contexto.
2. Como uma nova regra foi criada, você pode simplesmente dizer: **"leia o `docs/STATUS.md` e continue de onde paramos"** (ou configure um atalho no seu prompt inicial).
3. A própria IA abrirá o `STATUS.md`, descobrirá qual o plano em andamento, lerá as necessidades e seguirá programando sem precisar de colar o prompt gigante de novo.
4. Ao terminar uma tarefa, ordene que ela atualize o relatório em `docs/audits/` e edite o estado do `docs/STATUS.md`.

---

## 🛑 CHECKLIST DE REVISÃO E VALIDAÇÃO (Auditoria de Geração)

Conforme sua solicitação de ser minucioso, não ter preguiça e não alucinar, aqui está a checagem do que foi integrado:

1. **Agnóstico de Software:** O documento serve para SaaS, microsserviços, plataformas de dados ou APIs gerais, seja usando ecossistemas de alta performance ou APIs web modernas. *(Check)*
2. **Definição de Workflow:** O fluxo de ponta a ponta está descrito (Ideia -> Gemini cria o Plano -> Claude Executa -> TDD aprova -> Merge). *(Check)*
3. **Pilar de DDD:** Incluído. A IA executora é limitada a contextos delimitados. *(Check)*
4. **Pilar Hexagonal:** Incluído e convertido em regra inegociável no `.clauderules` e no Template de Planos. *(Check)*
5. **Pilar Clean Code & TDD:** Incluído como lei. A IA foi forçada a desenhar testes e tratar injeções de dependência *antes* de codar. Acrescentamos Observabilidade e Limite de Falhas (Max Retries). *(Check)*
6. **Robustez Operacional:** Inseridos fluxos anti-alucinação, exceções científicas (Spikes) e ciclo de CI estrito, blindando o desenvolvedor de espirais de erro da IA. *(Check)*
7. **Pronto para Começar:** Workflow de *Start-up* definido na Seção 7. Do PRD à arquitetura em um caminho coeso e prático. O Playbook agora funciona como um manual de engenharia completo e à prova de falhas. *(Check)*

---

## 9. Orquestração Multi-Agente (Agentic Parallelism & Skills)

Com o uso de clientes de linha de comando (como CLI do Claude ou Aider), você destrava a capacidade de usar a sua máquina como um "Orquestrador de Agentes" (semelhante ao Devin ou Replit). 

**O Problema do Token Bloat:** Entregar um plano monolítico para o agente esgota a sua janela de contexto e o deixa confuso ("hallucination").

**A Solução (Fan-Out / Fan-In):** O Arquiteto (Gemini) quebra o trabalho em Micro-Planos paralelos (Trilha A e Trilha B). Você (Diretor) pode abrir 2 terminais simultâneos rodando o `claude-cli`, um processando a Trilha A e outro a Trilha B.

### Regras de Ouro para Concorrência CLI (Boas Práticas Validadas):
1. **Isolamento Geográfico Absoluto (Zero-Conflict):** Agentes Paralelos NUNCA podem ler ou editar os mesmos arquivos. A Trilha A pode modificar o Frontend (`/src/ui`), enquanto a Trilha B monta os test containers (`/tests/infra`). 
2. **Uso de "Skills" em vez de Regras Globais:** A pasta `/docs/skills/` contém mini-checklists de tarefas comuns. Em vez de explicar como montar uma API FastAPI em todos os prompts, o plano ativo dirá à IA CLI: `"Invoque a skill docs/skills/fastapi-crud.md"`. A IA lê uma regra super minúscula (economia de tokens drástica) executando como um trabalhador de fábrica especialista.
3. **Escrita Linear, Leitura Paralela:** Múltiplos agentes podem ler seus arquivos do projeto ao mesmo tempo sem medo. Mas ao solicitar que codifiquem, o Arquiteto criará os Planos de Execução já sabendo que eles não conflitam as injeções de dependência.
4. **Fechamento (Fan-In):** Assim que os 2 terminais CLIs exibirem `SKILL CONCLUÍDA`, o Diretor (Você) envia os dois relatórios para o Arquiteto (Eu), e nós fazemos o plano de integração final.