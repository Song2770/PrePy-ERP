from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import List, Optional
from decimal import Decimal
from datetime import date
from database import get_db
from models.procurement import PurchaseOrder
from models.user import User
from utils.auth import verify_token

print("正在加载采购管理路由...")

router = APIRouter()
security = HTTPBearer()

class PurchaseOrderCreate(BaseModel):
    number: str
    supplier_id: int
    order_date: date
    expected_date: Optional[date] = None
    currency: str = "CNY"
    total_amount: Decimal = 0
    status: str = "待确认"

class PurchaseOrderResponse(BaseModel):
    id: int
    number: str
    supplier_id: int
    order_date: date
    expected_date: Optional[date]
    currency: str
    total_amount: Decimal
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

@router.get("/purchase-orders", response_model=List[PurchaseOrderResponse])
async def get_purchase_orders(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取采购订单列表"""
    print(f"获取采购订单列表，跳过: {skip}, 限制: {limit}")
    
    result = await db.execute(
        select(PurchaseOrder).offset(skip).limit(limit)
    )
    orders = result.scalars().all()
    
    return [PurchaseOrderResponse.model_validate(order) for order in orders]

@router.post("/purchase-orders", response_model=PurchaseOrderResponse)
async def create_purchase_order(
    order_data: PurchaseOrderCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """创建采购订单"""
    print(f"创建采购订单: {order_data.number}")
    
    # 检查订单号是否已存在
    result = await db.execute(
        select(PurchaseOrder).where(PurchaseOrder.number == order_data.number)
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="采购订单号已存在"
        )
    
    # 创建采购订单
    order = PurchaseOrder(**order_data.model_dump())
    
    db.add(order)
    await db.commit()
    await db.refresh(order)
    
    print(f"采购订单创建成功: {order.number}")
    return PurchaseOrderResponse.model_validate(order)

print("采购管理路由加载完成")