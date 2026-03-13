# ADR 001: Definição da Stack Tecnológica (MVP)
**Data:** 2026-03-12 | **Status:** Aceito

## Contexto
O MVP do *AgendaPro* precisa ser construído com foco em velocidade de resposta da IA (baixa latência e processamento assíncrono), facilidade de construção do Frontend web (dashboard) e uma persistência robusta porém ágil para gestão de usuários e locks de agenda.

## Decisão
Conforme alinhado no PRD, a Stack inegociável deste projeto será:
* **Backend:** Python + FastAPI (Para garantir performance e lidar bem com chamadas I/O Bound das LLMs).
* **Frontend:** React (Para criar o painel self-service do professor de maneira rápida).
* **Banco de Dados/Auth:** Supabase [PostgreSQL] (Garante BaaS ágil com fundação relacional forte para evitar falhas de concorrência em agendamentos).

## Consequências
* **Positivas:** Ecossistema Python é nativo para integração com as IAs. FastAPI traz validação de dados built-in (Pydantic). Supabase encurta semanas de desenvolvimento com Auth e Database prontos. 
* **Negativas:** A equipe/IA precisa gerenciar a comunicação correta entre os repositórios ou pastas separadas para Frontend e Backend, mantendo os contratos (APIs) bem definidos.
