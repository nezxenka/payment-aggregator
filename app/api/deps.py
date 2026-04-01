from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_access_token, hash_api_key
from app.models.merchant import Merchant

security = HTTPBearer()


async def get_current_merchant(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> Merchant:
    """Получение текущего мерчанта по JWT токену"""
    token = credentials.credentials
    payload = decode_access_token(token)
    
    merchant_id = payload.get("sub")
    if not merchant_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    
    merchant = db.query(Merchant).filter(Merchant.id == int(merchant_id)).first()
    if not merchant:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Merchant not found"
        )
    
    if not merchant.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Merchant account is inactive"
        )
    
    return merchant
