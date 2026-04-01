from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Dict, Any


class PaymentProvider(ABC):
    """Базовый класс для платежных провайдеров"""
    
    @abstractmethod
    async def create_payment(
        self,
        amount: Decimal,
        currency: str,
        description: str = None,
        metadata: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Создание платежа у провайдера"""
        pass
    
    @abstractmethod
    async def get_payment_status(self, provider_transaction_id: str) -> str:
        """Получение статуса платежа"""
        pass
    
    @abstractmethod
    async def refund_payment(
        self,
        provider_transaction_id: str,
        amount: Decimal = None
    ) -> Dict[str, Any]:
        """Возврат платежа"""
        pass
