from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base


class WebhookEndpoint(Base):
    """Webhook endpoints мерчантов"""
    __tablename__ = "webhook_endpoints"
    
    id = Column(Integer, primary_key=True, index=True)
    merchant_id = Column(Integer, ForeignKey("merchants.id"), nullable=False)
    
    url = Column(String, nullable=False)
    secret = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    merchant = relationship("Merchant", back_populates="webhooks")
    logs = relationship("WebhookLog", back_populates="endpoint")


class WebhookLog(Base):
    """Лог отправленных вебхуков"""
    __tablename__ = "webhook_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    endpoint_id = Column(Integer, ForeignKey("webhook_endpoints.id"), nullable=False)
    
    event_type = Column(String, nullable=False)
    payload = Column(Text, nullable=False)
    response_status = Column(Integer)
    response_body = Column(Text)
    
    attempts = Column(Integer, default=1)
    success = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    endpoint = relationship("WebhookEndpoint", back_populates="logs")
