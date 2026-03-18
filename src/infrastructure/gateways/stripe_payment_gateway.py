import logging

import stripe

from src.domain.errors import GatewayConnectionError
from src.domain.ports.payment_gateway import PaymentGateway

logger = logging.getLogger(__name__)


class StripePaymentGateway(PaymentGateway):
    def __init__(self, api_key: str, success_url: str, cancel_url: str):
        self._api_key = api_key
        self._success_url = success_url
        self._cancel_url = cancel_url

    def generate_payment_link(
        self,
        amount: int,
        currency: str,
        reference_id: str,
        description: str,
    ) -> str:
        try:
            session = stripe.checkout.Session.create(
                api_key=self._api_key,
                payment_method_types=["card"],
                line_items=[
                    {
                        "price_data": {
                            "currency": currency,
                            "unit_amount": amount,
                            "product_data": {"name": description},
                        },
                        "quantity": 1,
                    }
                ],
                mode="payment",
                client_reference_id=reference_id,
                metadata={"reference_id": reference_id},
                success_url=self._success_url,
                cancel_url=self._cancel_url,
            )
        except stripe.StripeError as exc:
            logger.error(
                "stripe_gateway_error",
                extra={"reference_id": reference_id, "error": str(exc)},
            )
            raise GatewayConnectionError(gateway="stripe", detail=str(exc)) from exc

        logger.info(
            "stripe_payment_link_generated",
            extra={"reference_id": reference_id, "session_id": session.id},
        )
        return session.url
