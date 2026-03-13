# ADR 002: Estratégia de Banco de Dados (Dev vs. Produção)
**Data:** 2026-03-13 | **Status:** Aceito

## Contexto
Após o Plano 001, foi necessário definir como a camada de Infraestrutura (Adaptadores) irá conectar as Portas do Domínio ao banco de dados. A questão central foi: usar um contêiner Docker com PostgreSQL puro para desenvolvimento, ou usar o Supabase diretamente em dois projetos separados?

## Decisão
**Usaremos o Supabase diretamente em dois projetos distintos:**
* `agendapro-dev` → Ambiente de desenvolvimento e testes de integração.
* `agendapro-prod` → Ambiente de produção.

A troca entre ambientes é feita exclusivamente por variável de ambiente (`DATABASE_URL` / `SUPABASE_URL` + `SUPABASE_KEY`). O código da aplicação **não muda nada** entre os ambientes, graças à Arquitetura Hexagonal.

## Consequências
* **Positivas:** Aproveitamos os recursos nativos do Supabase (Auth, Row Level Security, Realtime) desde o Dia 1 do MVP, sem reescrever na mão. Tier gratuito cobre o desenvolvimento inteiro. Zero configuração de Docker para banco de dados.
* **Negativas:** Os testes de integração dependem de conexão com internet. Mitigação: testes unitários (maioria) continuam usando mocks e não precisam de conexão.
