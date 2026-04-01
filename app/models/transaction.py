from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.core.database import Base


class TransactionStatus(str, enum.Enum):
    """Статусы транзакции"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"


class TransactionType(str, enum.Enum):
    """Типы транзакций"""
    PAYMENT = "payment"
    PAYOUT = "payout"
    REFUND = "refund"


class Transaction(Base):
    """Модель транзакции"""
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(String, unique=True, index=True, nullable=False)
    
    merchant_id = Column(Integer, ForeignKey("merchants.id"), nullable=False)
    
    amount = Column(Numeric(20, 8), nullable=False)
    currency = Column(String(3), nullable=False)
    status = Column(SQLEnum(TransactionStatus), default=TransactionStatus.PENDING)
    type = Column(SQLEnum(TransactionType), nullable=False)
    
    provider = Column(String, nullable=False)
    provider_transaction_id = Column(String, index=True)
    
    description = Column(String)
    customer_email = Column(String)
    
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    merchant = relationship("Merchant", back_populates="transactions")
