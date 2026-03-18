# Skill: Desenvolvimento de Regras de Negócio (Use Case / Domain)

> **Objetivo:** Você (Claude CLI) foi invocado como um Agente Especialista de Domínio. O seu papel é construir regras puras de negócio (Casos de Uso) sem NUNCA acoplar a dependências externas como Bancos de Dados REAIS ou frameworks Web pesados.

## 🛠 Contexto Limitado (Zero-Conflict)
Você tem permissão para ler e editar APENAS os arquivos nestes diretórios:
* `/src/core/usecases/`
* `/tests/unit/core/`
* `/src/core/ports/` (Leitura das interfaces para criar Fake Repositories nos testes)

## 📋 Passos Secretos (Checklist do Operário)
1. **Design do Fake/Mock:** Crie um "FakeRepository" (Em Memória) dentro do arquivo de teste em `/tests/unit/core/` simulando as Interfaces necessárias para rodar o cenário do teste unitário de forma ultrarrápida (sem IO).
2. **Setup do Teste (TDD - Red):** Escreva os testes para o caso de uso. Pense nas regras lógicas e nas exceções que o Domínio deve lançar (ex: erro de parâmetro, erro de lock já existente usando mocks).
3. **Implementação do Domínio (Green):** Codifique a classe de UseCase em `/src/core/usecases/`. A classe DEVE receber os repositórios através do seu construtor `__init__` (Injeção de Dependência). NUNCA importe ou instancie repositórios do Supabase diretamente aqui.
4. **Auditoria:** Rode os testes (ex: `pytest tests/unit/core/ -v`).

## 🛑 Condição de Saída
Assim que os testes unitários passarem, imprima no terminal:
**"✅ SKILL CONCLUÍDA: Casos de Uso Core implementados e testados unitariamente. Hand-off liberado em docs/audits/."** 
Crie o arquivo de audit e aguarde a próxima instrução humana.
