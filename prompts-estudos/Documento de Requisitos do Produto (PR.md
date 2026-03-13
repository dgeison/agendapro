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

### 3. Casos de Uso e Regras de Negócio (MVP)

* **Atendimento e Quebra de Gelo:** A IA responde instantaneamente, entende o contexto do aluno e apresenta a metodologia do professor.
* **Agendamento Inteligente (Aulas Avulsas):** A IA cruza a disponibilidade do aluno com os horários livres no calendário do professor e sugere opções. No MVP, o foco será exclusivamente em vendas de aulas avulsas.
* **Prevenção de Double Booking (Lock de Agenda):** Ao sugerir um horário e gerar o link de pagamento, a IA aplica um *lock* (bloqueio temporário) de 10 minutos naquele slot do banco de dados. Se o pagamento não for confirmado, o horário volta a ficar disponível.
* **Remarcação e Cancelamento:** O aluno pode solicitar remarcação diretamente via WhatsApp com até 24h de antecedência. Prazos menores que este geram um aviso da IA de que a aula não é reembolsável, conforme as regras do professor.
* **Lembretes Automáticos:** Disparo de notificação no WhatsApp 2 horas antes do início da sessão.

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