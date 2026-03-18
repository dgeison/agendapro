# Plano de Execução: 011a - Gateway de Faturas Stripe (Trilha A)

> 🏗️ **AUTORIA: IA ESTRATÉGICA (ANTIGRAVITY) - FASE 2: FATURAMENTO**
> *Iniciando a ponte financeira do projeto. A IA precisa ter um botão de "Gerar Fatura". Precisamos construir esse botão.*

## 1. Objetivo do Negócio
O sistema precisa de uma maneira de emitir Links de Pagamento transparentes do Stripe associados a um Aluno e ao seu pacote/aula.

## 2. Instruções Especiais de Execução
* 🎯 **Skill Demandada:** Você deve carregar e seguir rigidamente `/docs/skills/gateway-adapter.md`
* ⚠️ **Restrição:** Mexa APENAS no isolamento do Adapter. Não crie Webhooks, Rotas FastAPI nem UseCases lógicos e não altere a camada de BD.

## 3. Arquitetura Exigida
* **Porta (Interface) Esperada:** `/src/domain/ports/payment_gateway.py` (Crie-a).
    - Método a declarar: `generate_payment_link(amount: int, currency: str, reference_id: str, description: str) -> str`
* **Adaptador a criar:** `/src/infrastructure/gateways/stripe_payment_gateway.py`
    - O `reference_id` será nossa variável mais preciosa, ela entrará no `metadata` ou no `client_reference_id` do Stripe. Assim que o pagamento bater de volta no webhook, saberemos de quem é a aula paga.

## 4. O que testar (TDD Oobrigatório)
* Escreva testes no módulo `/tests/integration/` usando a biblioteca `pytest-mock` ou o próprio objeto Mock do Python encapsulando `stripe.checkout.Session.create`.
* O Teste principal passa um `reference_id` bobo e verifica se a string e os campos estão sendo repassados da SDK para o output, e retornando uma URL formatada simulada.

## 5. Fechamento
Ao atingir a Cobertura Verde nos mocks, finalize sua participação preenchendo o Handoff de infraestrutura.
