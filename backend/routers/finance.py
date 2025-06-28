from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import List, Optional
from decimal import Decimal
from datetime import date
from database import get_db
from models.finance import Invoice, Payment
from models.user import User
from utils.auth import verify_token

print("正在加载财务管理路由...")

router = APIRouter()
security = HTTPBearer()

class InvoiceCreate(BaseModel):
    number: str
    invoice_type: str  # 销售发票/采购发票
    partner_id: int  # 客户或供应商ID
    invoice_date: date
    due_date: Optional[date] = None
    currency: str = "CNY"
    subtotal: Decimal = 0
    tax_amount: Decimal = 0
    total_amount: Decimal = 0
    status: str = "草稿"

class InvoiceResponse(BaseModel):
    id: int
    number: str
    invoice_type: str
    partner_id: int
    invoice_date: date
    due_date: Optional[date]
    currency: str
    subtotal: Decimal
    tax_amount: Decimal
    total_amount: Decimal
    status: str
    created_at: str
    
    class Config:
        from_attributes = True

class PaymentCreate(BaseModel):
    number: str
    payment_type: str  # 收款/付款
    partner_id: int
    payment_date: date
    amount: Decimal
    currency: str = "CNY"
    payment_method: str = "银行转账"
    reference: Optional[str] = None
    status: str = "已确认"

class PaymentResponse(BaseModel):
    id: int
    number: str
    payment_type: str
    partner_id: int
    payment_date: date
    amount: Decimal
    currency: str
    payment_method: str
    reference: Optional[str]
    status: str
    created_at: str
    
    class Config:
        from_attributes = True

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    """获取当前用户"""
    payload = verify_token(credentials.credentials)
    username = payload.get("sub")
    
    result = await db.execute(
        select(User).where(User.username == username)
    )
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在"
        )
    
    return user

@router.get("/invoices", response_model=List[InvoiceResponse])
async def get_invoices(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取发票列表"""
    print(f"获取发票列表，跳过: {skip}, 限制: {limit}")
    
    result = await db.execute(
        select(Invoice).offset(skip).limit(limit)
    )
    invoices = result.scalars().all()
    
    return [InvoiceResponse.model_validate(invoice) for invoice in invoices]

@router.post("/invoices", response_model=InvoiceResponse)
async def create_invoice(
    invoice_data: InvoiceCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """创建发票"""
    print(f"创建发票: {invoice_data.number}")
    
    # 检查发票号是否已存在
    result = await db.execute(
        select(Invoice).where(Invoice.number == invoice_data.number)
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="发票号已存在"
        )
    
    # 创建发票
    invoice = Invoice(**invoice_data.model_dump())
    
    db.add(invoice)
    await db.commit()
    await db.refresh(invoice)
    
    print(f"发票创建成功: {invoice.number}")
    return InvoiceResponse.model_validate(invoice)

@router.get("/payments", response_model=List[PaymentResponse])
async def get_payments(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取付款记录列表"""
    print(f"获取付款记录列表，跳过: {skip}, 限制: {limit}")
    
    result = await db.execute(
        select(Payment).offset(skip).limit(limit)
    )
    payments = result.scalars().all()
    
    return [PaymentResponse.model_validate(payment) for payment in payments]

@router.post("/payments", response_model=PaymentResponse)
async def create_payment(
    payment_data: PaymentCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """创建付款记录"""
    print(f"创建付款记录: {payment_data.number}")
    
    # 检查付款号是否已存在
    result = await db.execute(
        select(Payment).where(Payment.number == payment_data.number)
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="付款号已存在"
        )
    
    # 创建付款记录
    payment = Payment(**payment_data.model_dump())
    
    db.add(payment)
    await db.commit()
    await db.refresh(payment)
    
    print(f"付款记录创建成功: {payment.number}")
    return PaymentResponse.model_validate(payment)

print("财务管理路由加载完成")