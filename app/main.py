from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.routes import auth, payments, merchant

app = FastAPI(
    title="Payment Aggregator API",
    description="Платежный агрегатор для приема платежей",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Роуты
app.include_router(auth.router)
app.include_router(payments.router)
app.include_router(merchant.router)


@app.get("/")
async def root():
    return {"message": "Payment Aggregator API", "status": "running"}


@app.get("/health")
async def health():
    return {"status": "healthy"}
