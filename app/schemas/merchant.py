from pydantic import BaseModel, EmailStr
from datetime import datetime
from decimal import Decimal


class MerchantCreate(BaseModel):
    """Схема для создания мерчанта"""
    email: EmailStr
    company_name: str
    password: str


class MerchantLogin(BaseModel):
    """Схема для логина"""
    email: EmailStr
    password: str


class MerchantResponse(BaseModel):
    """Схема ответа с данными мерчанта"""
    id: int
    email: str
    company_name: str
    balance: Decimal
    is_active: bool
    is_verified: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class ApiKeyResponse(BaseModel):
    """Схема ответа с API ключом"""
    api_key: str
    message: str
