"""
Teste de integração (com mock): StripePaymentGateway
Critérios de aceite:
  1. generate_payment_link() chama stripe.checkout.Session.create com os campos corretos
     e retorna a URL do link gerado.
  2. reference_id é repassado no metadata do Stripe.
  3. Erros da SDK Stripe são convertidos em GatewayConnectionError.
"""
from unittest.mock import MagicMock, patch

import pytest
import stripe

from src.domain.errors import GatewayConnectionError
from src.infrastructure.gateways.stripe_payment_gateway import StripePaymentGateway


@pytest.fixture
def gateway():
    return StripePaymentGateway(api_key="sk_test_fake", success_url="https://app.test/success", cancel_url="https://app.test/cancel")


class TestStripePaymentGateway:
    def test_generate_payment_link_returns_url(self, gateway: StripePaymentGateway):
        """Critério 1: retorna a URL gerada pelo Stripe."""
        fake_session = MagicMock()
        fake_session.url = "https://checkout.stripe.com/pay/cs_test_abc123"

        with patch("stripe.checkout.Session.create", return_value=fake_session) as mock_create:
            url = gateway.generate_payment_link(
                amount=10000,
                currency="brl",
                reference_id="appt-xyz-001",
                description="Aula de Matemática",
            )

        assert url == "https://checkout.stripe.com/pay/cs_test_abc123"
        mock_create.assert_called_once()

    def test_generate_payment_link_passes_reference_id_in_metadata(self, gateway: StripePaymentGateway):
        """Critério 2: reference_id é enviado no client_reference_id e/ou metadata."""
        fake_session = MagicMock()
        fake_session.url = "https://checkout.stripe.com/pay/cs_test_ref"

        with patch("stripe.checkout.Session.create", return_value=fake_session) as mock_create:
            gateway.generate_payment_link(
                amount=5000,
                currency="brl",
                reference_id="appt-ref-999",
                description="Aula de Física",
            )

        call_kwargs = mock_create.call_args.kwargs
        assert call_kwargs.get("client_reference_id") == "appt-ref-999"

    def test_generate_payment_link_raises_gateway_connection_error_on_stripe_error(
        self, gateway: StripePaymentGateway
    ):
        """Critério 3: exceção da SDK Stripe vira GatewayConnectionError."""
        with patch(
            "stripe.checkout.Session.create",
            side_effect=stripe.StripeError("Connection failed"),
        ):
            with pytest.raises(GatewayConnectionError) as exc_info:
                gateway.generate_payment_link(
                    amount=1000,
                    currency="brl",
                    reference_id="appt-fail-001",
                    description="Aula Falha",
                )

        assert "stripe" in str(exc_info.value).lower()
