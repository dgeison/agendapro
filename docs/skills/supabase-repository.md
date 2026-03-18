# Skill: Repositório Supabase (Padrão Hexagonal / Adapter)

> **Objetivo:** Você (Claude CLI) foi invocado como um Agente Especialista de Infraestrutura. Seu papel é APENAS implementar classes que implementam as Interfaces (Ports) do domínio usando o cliente do banco de dados (Supabase).
> **Atenção:** Mantenha o seu output e raciocínio minúsculos. Não discuta a arquitetura.

## 🛠 Contexto Limitado (Zero-Conflict)
Você tem permissão para ler e editar APENAS os arquivos nestes diretórios:
* `/src/infra/repositories/`
* `/tests/integration/infra/`
* `/src/core/ports/` (Apenas leitura da Interface exigida pelo domínio)

## 📋 Passos Secretos (Checklist do Operário)
1. **Verificação (Read-Only):** Leia o arquivo da Interface (Port) no diretório `/src/core/ports/` correspondente à entidade do Plano Ativo.
2. **Setup do Teste (TDD):** Crie o teste de integração em `/tests/integration/infra/test_[entidade]_supabase_repository.py`. Inicialmente este teste DEVE falhar (Red). Moke a conexão HTTP ou use o test container (de acordo com a convenção de testes do repositório).
3. **Implementação (Green):** Codifique a classe de repositório (Adapter) em `/src/infra/repositories/[entidade]_supabase_repository.py`. Ela DEVE obrigatoriamente herdar a Interface do Core. Use a biblioteca oficial (ou httpx) pré-configurada no projeto para chamar a API REST do Supabase.
4. **Tratamento de Erros:** Respostas de erro da API (400, 401, 500) devem ser capturadas e convertidas em Exceções customizadas mapeadas pelo Domínio (ex: `RepositoryConnectionError`).
5. **Auditoria:** Rode os testes (ex: `pytest tests/integration/infra/test_[entidade]_supabase_repository.py -v`). 

## 🛑 Condição de Saída
Assim que os testes dessa camada passarem (Green), não mexa em endpoints (FastAPI) ou casos de uso (Use Cases). Pare e imprima no terminal:
**"✅ SKILL CONCLUÍDA: Repositório Supabase para [Entidade] implementado e testado. Hand-off liberado em docs/audits/."** 
Crie o arquivo de audit e aguarde a próxima instrução humana.
