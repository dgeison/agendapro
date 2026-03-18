# Documento de Requisitos do Produto (PRD) - Versão Final (v1.0)

**Produto:** AgendaPro (SaaS de Agendamento e Cobrança via WhatsApp com IA)
**Nicho Inicial:** Professores Autônomos (Idiomas, Reforço Escolar, Mentoria)

### 1. Visão Geral e Objetivo

Desenvolver uma plataforma SaaS que automatiza o agendamento de aulas, a negociação de horários e a cobrança de pagamentos, atuando 100% dentro do WhatsApp do professor por meio de uma IA conversacional com memória de contexto. O objetivo é eliminar o trabalho administrativo, reduzir faltas e aumentar a conversão de novos alunos.

### 2. O Problema (A Dor do Usuário)

* **Demora na Resposta:** O professor perde alunos porque está em aula e não pode responder imediatamente.
* **Gestão Caótica:** Conflitos de agenda, esquecimentos e dificuldade em conciliar horários.
* **Fricção na Cobrança:** Desconforto ao cobrar pagamentos atrasados ou gerenciar comprovantes manuais.
* **Falta de Retenção (No-show):** Alunos que esquecem o horário da aula e não avisam.

### 3. Casos de Uso e Regras de Negócio (Visão de Produto)

O diferencial absoluto do SaaS será a IA agir como "Secretária e Financeiro" fluida. O sistema deve suportar as seguintes interações conversacionais:

#### 3.1 Pelo Lado do Professor (Gestão Ativa)
* *"Tenho aula hoje?"* -> A IA lista a agenda do dia cruzando com Google Calendar e DB.
* *"Marca aula com fulano"* -> A IA força o Slot na agenda e avisa o aluno.
* *"Veja as aulas disponíveis do aluno"* -> Verifica saldo (pacotes em haver).
* *"Gere relação de aulas/pagamentos"* -> A IA compila um mini relatório de faturamento do mês ou do aluno.
* *"Gere pagamento e cobre ele"* -> A IA cria ativamente o webhook do Stripe e manda pro aluno via WhatsApp.
* *"O aluno X está em dias?"* -> A IA checa o status de faturas no Stripe.

#### 3.2 Pelo Lado do Aluno (Self-Service)
* *"Quero agendar"* -> A IA cruza com os `Available Slots` do professor.
* *"Quero pagar"* -> IA busca faturas em aberto e gera o link.
* *"Quantas aulas ainda tenho?"* -> IA exibe o saldo do pacote pago.
* *"Deo alguma coisa? Gere o boleto"* -> IA checa débitos e emite a cobrança.

#### 3.3 Regras Core do Sistema (Obrigatórias)
* **Prevenção de Double Booking (Lock de Agenda):** Ao sugerir um horário e gerar o link de pagamento, a IA aplica um *lock* (bloqueio temporário) de 10 minutos naquele slot do banco de dados. Se o pagamento não confirmou (via webhooks do Stripe), destrava.
* **Remarcação e Cancelamento:** O aluno pode solicitar remarcação diretamente via WhatsApp com até 24h de antecedência. Prazos menores que este geram um aviso da IA de que a aula não é reembolsável, conforme as regras cadastradas no Onboarding do professor.
* **Lembretes Automáticos (CronJobs):** Disparo de notificação no WhatsApp 2 horas antes do início da sessão.

### 4. Escopo Técnico e Arquitetura do MVP

* **Backend:** Python com FastAPI (essencial para alta velocidade e processamento assíncrono das LLMs).
* **Frontend (Painel do Professor):** React para um dashboard rápido e responsivo.
* **Banco de Dados e Autenticação:** Supabase (PostgreSQL) para garantir robustez relacional e gestão de usuários.
* **Integrações Externas Obrigatórias:**
* Meta Cloud API (WhatsApp Business).
* Stripe (Gateway para geração de links de pagamento e webhooks de confirmação).
* Google Calendar (Sincronização bidirecional de agenda).



### 5. Onboarding do Professor (Self-Service)

A entrada do usuário no sistema deve ser feita em menos de 10 minutos via dashboard web. O professor preencherá um formulário simples que servirá de "System Prompt" para a sua IA:

* Nome e especialidade (ex: Professor de Inglês para Negócios).
* Valor da hora/aula.
* Link da sala de videoconferência (Zoom/Meet).
* Tolerância de atraso e tom de voz desejado para a IA.

### 6. Métricas de Sucesso do MVP

* **Tempo de Resposta da IA:** < 5 segundos.
* **Taxa de Conversão:** % de conversas iniciadas que resultam em pagamento confirmado.
* **Engajamento no Onboarding:** % de professores que completam o setup inicial sem precisar de suporte humano.