from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal
from typing import Optional

from app.models.transaction import TransactionStatus, TransactionType


class TransactionCreate(BaseModel):
    """Схема для создания транзакции"""
    amount: Decimal
    currency: str
    provider: str
    description: Optional[str] = None
    customer_email: Optional[str] = None


class TransactionResponse(BaseModel):
    """Схема ответа транзакции"""
    id: int
    external_id: str
    amount: Decimal
    currency: str
    status: TransactionStatus
    type: TransactionType
    provider: str
    description: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True
