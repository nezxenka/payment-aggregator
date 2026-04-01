from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.api.deps import get_current_merchant
from app.models.merchant import Merchant
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionResponse
from app.services.payment_service import PaymentService

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.post("/", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
async def create_payment(
    payment_data: TransactionCreate,
    merchant: Merchant = Depends(get_current_merchant),
    db: Session = Depends(get_db)
):
    """Создание нового платежа"""
    
    service = PaymentService(db)
    
    transaction = await service.create_payment(
        merchant=merchant,
        amount=payment_data.amount,
        currency=payment_data.currency,
        provider_name=payment_data.provider,
        description=payment_data.description,
        customer_email=payment_data.customer_email
    )
    
    return transaction


@router.get("/", response_model=List[TransactionResponse])
async def list_payments(
    merchant: Merchant = Depends(get_current_merchant),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """Список транзакций мерчанта"""
    
    transactions = db.query(Transaction).filter(
        Transaction.merchant_id == merchant.id
    ).offset(skip).limit(limit).all()
    
    return transactions
