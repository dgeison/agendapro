# 🧭 STATUS DO PROJETO E PRÓXIMAS AÇÕES

> **IA EXECUTORA:** Este é o seu ponto central de verdade sobre o estado atual do projeto. 
> Sempre que iniciar uma sessão, leia este arquivo para entender onde paramos e qual é a sua próxima tarefa. Atualize este arquivo quando concluir uma entrega importante ou travar em um problema.

## 📍 Estado Atual
- **Último Plano Concluído:** `docs/plans/006-onboarding-professor.md` (Ver relatório final em `docs/audits/006_01-relatorio_onboarding-professor.md`).
- **Fase de Desenvolvimento:** MVP Backend (FastAPI + Supabase).

## 🎯 Planos Ativos (Orquestração Multi-Agente)
- **🚀 Trilha A (Gateway API):** *Livre/Nenhum plano ativo.* (Humano: Atribua aqui o próximo plano)
- **🚀 Trilha B (Backend/Infra):** *Livre/Nenhum plano ativo.* (Humano: Atribua aqui o próximo plano)

> *Nota: Você pode operar em uma única trilha ou engatilhar múltiplos Agentes (ex: abrir 2 terminais com o Claude CLI simultaneamente e mandar um ler a Trilha A e outro a Trilha B, economizando tempo. Nunca atribua a Trilha A e B para mexerem nos mesmos arquivos).*

## 🚀 Próxima Ação da IA
1. Aguardar o humano fornecer o próximo plano em uma (ou ambas) das Trilhas acima.
2. Assim que o humano liberar a execução em um terminal:
    - Verifique em qual Trilha o terminal foi designado a operar.
    - Se o plano fizer menção a uma **Skill** em `docs/skills/`, leia ela ANTES para saber como implementar o padrão e **reduzir o gasto de tokens**.
3. Iniciar a execução do plano seguindo rigorosamente o `.clauderules` (TDD, Clean Code, Arquitetura Hexagonal).
4. Ao concluir (ou se bloquear permanentemente): gerar o relatório em `docs/audits/` e **atualizar ESSE arquivo `STATUS.md`** refletindo as mudanças de estado.

## 📝 Histórico Recente de Progressos
- ✅ 011a: Gateway de Faturas Stripe (Adapter isolado)
- ✅ 011: Gestão de Saldo de Pacotes (Repositório Supabase)
- ✅ 010: Gestão de Saldo de Créditos (Infra/DB)
- ✅ 009: Injeção e Endpoint de Agendamentos (Fan-In API)
- ✅ 008a: Regras de Negócio de Agendamento (Core UseCase)
- ✅ 007b: Persistência de Agendamentos (Repositório Supabase)
- ✅ 006: Onboarding Professor
- ✅ 005: Expiração Locks Agenda
- ✅ 004: Autenticação JWT
- ✅ 001: Setup Domínio
