# Plano de Execução: 010 - Gestão de Saldo de Créditos (Trilha B - Infra/DB)

> 🏗️ **AUTORIA: IA ESTRATÉGICA (ANTIGRAVITY)**
> *Este plano inicia a Fase de "Economia de Aulas". Nosso foco agora é construir a fundação no banco de dados para gerenciar pacotes/créditos de alunos.*

## 1. Objetivo do Negócio
Criar a entidade que represente o saldo de aulas de um aluno. Quando a IA perguntar "Quantas aulas eu tenho?", precisaremos ler do Supabase os "Créditos Disponíveis". Esse plano aborda a Porta (Interface) e o Adaptador (Repository).

## 2. Instruções Especiais de Execução
* 🎯 **Skill Demandada:** Reutilize a regra lida em `/docs/skills/supabase-repository.md`.
* ⚠️ **Restrição Geográfica:** Fique estritamente na camada de repositórios e testes de integração. (NÃO crie a API ou UseCases ainda).

## 3. Arquitetura Exigida
* **Nova Entidade:** `StudentPackage` (Pacote do Aluno).
* **Porta (Interface) Esperada:** `/src/core/ports/package_repository.py`
  - Criar um método abstrato: `get_student_balance(student_id: str) -> int`
  - Criar um método abstrato: `add_credits(student_id: str, amount: int) -> dict`
* **Adaptador à criar:** `/src/infra/repositories/supabase_package_repository.py`
  - Deve herdar da porta acima e bater na tabela `student_packages` do Supabase usando chamada RPC ou query direta (via `supabase_client`).

## 4. Bloqueio Antecipado (Atenção Claude CLI!)
* Antes de codificar os testes de integração, crie a classe vazia e inicie os testes (TDD Red). 
* Você PROVAVELMENTE enfrentará o erro `PGRST205` de tabela inexistente no Supabase, assim como no Plano 007b. 
* Se isso ocorrer, capture a Stack Trace no relatório de Auditoria e peça ao Humano para criar essa tabela com os campos `id`, `student_id`, `credits_balance`, `created_at` e `updated_at`.

## 5. Fechamento
Ao concluir e/ou bater na parede da tabela inexistente, documente as etapas da sua Skill em `docs/audits/` e atualize o `STATUS.md` para devolver a Trilha ao humano.
