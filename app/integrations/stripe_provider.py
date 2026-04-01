from decimal import Decimal
from typing import Dict, Any
import stripe

from app.integrations.base import PaymentProvider
from app.core.config import settings

stripe.api_key = settings.STRIPE_API_KEY


class StripeProvider(PaymentProvider):
    """Интеграция со Stripe"""
    
    async def create_payment(
        self,
        amount: Decimal,
        currency: str,
        description: str = None,
        metadata: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Создание платежа в Stripe"""
        
        amount_cents = int(amount * 100)
        
        payment_intent = stripe.PaymentIntent.create(
            amount=amount_cents,
            currency=currency.lower(),
            description=description,
            metadata=metadata or {}
        )
        
        return {
            "provider_transaction_id": payment_intent.id,
            "status": payment_intent.status,
            "client_secret": payment_intent.client_secret
        }
    
    async def get_payment_status(self, provider_transaction_id: str) -> str:
        """Получение статуса платежа"""
        payment_intent = stripe.PaymentIntent.retrieve(provider_transaction_id)
        return payment_intent.status
    
    async def refund_payment(
        self,
        provider_transaction_id: str,
        amount: Decimal = None
    ) -> Dict[str, Any]:
        """Возврат платежа"""
        refund_data = {"payment_intent": provider_transaction_id}
        
        if amount:
            refund_data["amount"] = int(amount * 100)
        
        refund = stripe.Refund.create(**refund_data)
        
        return {
            "refund_id": refund.id,
            "status": refund.status
        }
