from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    generate_api_key,
    hash_api_key
)
from app.models.merchant import Merchant
from app.schemas.merchant import MerchantCreate, MerchantLogin, MerchantResponse, ApiKeyResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=MerchantResponse, status_code=status.HTTP_201_CREATED)
async def register(merchant_data: MerchantCreate, db: Session = Depends(get_db)):
    """Регистрация нового мерчанта"""
    
    # Проверка существования
    existing = db.query(Merchant).filter(Merchant.email == merchant_data.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Создание мерчанта
    merchant = Merchant(
        email=merchant_data.email,
        company_name=merchant_data.company_name,
        hashed_password=get_password_hash(merchant_data.password)
    )
    
    db.add(merchant)
    db.commit()
    db.refresh(merchant)
    
    return merchant


@router.post("/login")
async def login(credentials: MerchantLogin, db: Session = Depends(get_db)):
    """Логин мерчанта"""
    
    merchant = db.query(Merchant).filter(Merchant.email == credentials.email).first()
    if not merchant or not verify_password(credentials.password, merchant.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    if not merchant.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive"
        )
    
    access_token = create_access_token(data={"sub": str(merchant.id)})
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
