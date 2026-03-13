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
