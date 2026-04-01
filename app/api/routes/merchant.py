from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_merchant
from app.core.security import generate_api_key, hash_api_key
from app.models.merchant import Merchant
from app.schemas.merchant import MerchantResponse, ApiKeyResponse

router = APIRouter(prefix="/merchant", tags=["Merchant"])


@router.get("/me", response_model=MerchantResponse)
async def get_me(merchant: Merchant = Depends(get_current_merchant)):
    """Получение информации о текущем мерчанте"""
    return merchant


@router.post("/api-key", response_model=ApiKeyResponse)
async def generate_new_api_key(
    merchant: Merchant = Depends(get_current_merchant),
    db: Session = Depends(get_db)
):
    """Генерация нового API ключа"""
    
    api_key = generate_api_key()
    merchant.api_key_hash = hash_api_key(api_key)
    
    db.commit()
    
    return ApiKeyResponse(
        api_key=api_key,
        message="API key generated. Save it securely, it won't be shown again."
    )