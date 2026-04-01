from datetime import datetime

from app.tasks.celery_app import celery_app
from app.core.database import SessionLocal
from app.models.transaction import Transaction, TransactionStatus
from app.services.payment_service import PaymentService


@celery_app.task
def check_payment_status(transaction_id: int):
    """Проверка статуса платежа у провайдера"""
    
    db = SessionLocal()
    try:
        transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
        if not transaction or not transaction.provider_transaction_id:
            return
        
        service = PaymentService(db)
        provider = service.get_provider(transaction.provider)
        
        status = provider.get_payment_status(transaction.provider_transaction_id)
        
        if status == "succeeded":
            transaction.status = TransactionStatus.COMPLETED
            transaction.completed_at = datetime.utcnow()
        elif status == "failed":
            transaction.status = TransactionStatus.FAILED
        
        db.commit()
        
    finally:
        db.close()
