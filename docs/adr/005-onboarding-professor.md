# ADR 005: Estratégia de Onboarding do Professor — Vinculação JWT → Perfil
**Data:** 2026-03-14 | **Status:** Aceito

## Contexto

O Supabase Auth gerencia autenticação, mas não perfis de negócio. Quando um professor se registra via Supabase Auth, existe um usuário com UUID no auth, mas nenhum registro na tabela `professors`. Sem essa vinculação, nenhum endpoint de negócio sabe a qual professor o token pertence. É necessário um mecanismo de criação de perfil que ligue o `sub` do JWT (UUID do Supabase Auth) ao registro `Professor` no banco. Duas abordagens foram avaliadas: (A) criar o Professor automaticamente via trigger no banco ao registrar no Supabase Auth — viola DDD ao colocar lógica de negócio no banco; (B) endpoint explícito `POST /professors/me` chamado pelo professor após o primeiro login — mantém DDD e é testável.

## Decisão

Usar endpoint explícito `POST /professors/me` (Opção B). O `professor_id` vem do JWT (mesmo padrão já estabelecido no Plano 004). O endpoint cria o perfil do professor ligando o UUID do auth ao registro de domínio. Um segundo endpoint `GET /professors/me` permite leitura do perfil. Ambos seguem a Arquitetura Hexagonal: novos use cases em `src/application/`, sem lógica de negócio na camada de entrada.

## Consequências

* **Positivas:** Professor controla quando completa o onboarding. Totalmente testável via mocks. Reutiliza o padrão de auth do Plano 004 sem alterações. Sem dependência de triggers ou lógica no banco.
* **Negativas:** Requer que o frontend faça uma chamada explícita após registro. Se o professor não chamar `POST /professors/me`, endpoints subsequentes que buscam o perfil retornarão 404.
