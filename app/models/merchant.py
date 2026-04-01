from sqlalchemy import Column, Integer, String, Boolean, DateTime, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base


class Merchant(Base):
    """Модель мерчанта - клиента платформы"""
    __tablename__ = "merchants"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    company_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    api_key_hash = Column(String, unique=True, index=True)
    
    # Балансы
    balance = Column(Numeric(20, 8), default=0)
    
    # Статус
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    transactions = relationship("Transaction", back_populates="merchant")
    webhooks = relationship("WebhookEndpoint", back_populates="merchant")
