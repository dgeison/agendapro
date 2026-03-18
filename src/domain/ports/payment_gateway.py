from abc import ABC, abstractmethod


class PaymentGateway(ABC):
    @abstractmethod
    def generate_payment_link(
        self,
        amount: int,
        currency: str,
        reference_id: str,
        description: str,
    ) -> str:
        """
        Gera um link de pagamento no gateway externo.

        Args:
            amount: Valor em centavos (ex: 10000 = R$100,00).
            currency: Código ISO 4217 (ex: 'brl').
            reference_id: Identificador interno (ex: appointment_id) gravado nos metadados do gateway.
            description: Descrição exibida ao pagador.

        Returns:
            URL do link de pagamento gerado.
        """
        raise NotImplementedError
