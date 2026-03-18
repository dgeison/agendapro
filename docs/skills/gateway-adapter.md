# Skill: Integração Gateway de Pagamento (Adapter)

> **Objetivo:** Você (Claude CLI) foi invocado como um Agente Especialista de Integração de Pagamento. Gateways de pagamento são 'Detalhes de Infraestrutura'. Isolar lib de terceiros aqui é lei. Nenhuma regra de negócio deve vazar.

## 🛠 Contexto Limitado (Zero-Conflict)
Você tem permissão para ler e editar APENAS os arquivos nestes diretórios:
* `/src/infrastructure/gateways/`
* `/tests/integration/infrastructure/`
* `/src/domain/ports/` (Read-only para a interface correspondente)

## 📋 Passos Secretos (Checklist do Operário)
1. **Verificação:** Cheque a interface `PaymentGateway` correspondente ao plano no diretório de ports.
2. **Setup TDD:** Escreva o teste (ex: `test_stripe_payment_gateway.py`). Não faça requests REAIS pro Stripe nos testes que consumam limite do cartão. Use mock profundo (ex: `unittest.mock.patch` na SDK oficial) ou os retornos dummy permitidos pela documentação.
3. **Implementação (Adapter):** Codifique a classe `StripePaymentGateway`. 
   - Toda invocação oficial à SDK (ex: `stripe.checkout.Session.create`) ocorre e se encerra aqui, encapsulada.
   - Traduza dejetos e Exceções de rede do provedor de pagamento para uma exceção interna do domínio (ex: `GatewayConnectionError`).
4. **Auditoria:** Rode a suíte de integração e limpe Warnings desnecessários.

## 🛑 Condição de Saída
Assim que os testes passarem, imprima: **"✅ SKILL CONCLUÍDA: Adapter Gateway Stripe finalizado e isolado da aplicação. Hand-off liberado em docs/audits/."** 
Crie a avaliação final no relatório de auditoria e feche a Trilha.
