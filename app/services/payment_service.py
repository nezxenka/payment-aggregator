from sqlalchemy.orm import Session
from decimal import Decimal
import uuid

from app.models.transaction import Transaction, TransactionStatus, TransactionType
from app.models.merchant import Merchant
from app.integrations.base import PaymentProvider
from app.integrations.stripe_provider import StripeProvider


class PaymentService:
    """Сервис для обработки платежей"""
    
    def __init__(self, db: Session):
        self.db = db
        self.providers = {
            "stripe": StripeProvider()
        }
    
    def get_provider(self, provider_name: str) -> PaymentProvider:
        """Получение провайдера по имени"""
        provider = self.providers.get(provider_name)
        if not provider:
            raise ValueError(f"Provider {provider_name} not supported")
        return provider
    
    async def create_payment(
        self,
        merchant: Merchant,
        amount: Decimal,
        currency: str,
        provider_name: str,
        description: str = None,
        customer_email: str = None
    ) -> Transaction:
        """Создание платежа"""
        
        transaction = Transaction(
            external_id=str(uuid.uuid4()),
            merchant_id=merchant.id,
            amount=amount,
            currency=currency,
            type=TransactionType.PAYMENT,
            status=TransactionStatus.PENDING,
            provider=provider_name,
            description=description,
            customer_email=customer_email
        )
        
        self.db.add(transaction)
        self.db.commit()
        self.db.refresh(transaction)
        
        return transaction
