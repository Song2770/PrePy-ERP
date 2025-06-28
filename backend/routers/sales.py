from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import List, Optional
from decimal import Decimal
from datetime import date
from database import get_db
from models.sales import SalesOrder, SalesOrderLine
from models.user import User
from utils.auth import verify_token

print("正在加载销售管理路由...")

router = APIRouter()
security = HTTPBearer()

class SalesOrderCreate(BaseModel):
    number: str
    customer_id: int
    order_date: date
    delivery_date: Optional[date] = None
    currency: str = "CNY"
    total_amount: Decimal = 0
    status: str = "待确认"

class SalesOrderResponse(BaseModel):
    id: int
    number: str
    customer_id: int
    order_date: date
    delivery_date: Optional[date]
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

@router.get("/orders", response_model=List[SalesOrderResponse])
async def get_sales_orders(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取销售订单列表"""
    print(f"获取销售订单列表，跳过: {skip}, 限制: {limit}")
    
    result = await db.execute(
        select(SalesOrder).offset(skip).limit(limit)
    )
    orders = result.scalars().all()
    
    return [SalesOrderResponse.model_validate(order) for order in orders]

@router.post("/orders", response_model=SalesOrderResponse)
async def create_sales_order(
    order_data: SalesOrderCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """创建销售订单"""
    print(f"创建销售订单: {order_data.number}")
    
    # 检查订单号是否已存在
    result = await db.execute(
        select(SalesOrder).where(SalesOrder.number == order_data.number)
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="订单号已存在"
        )
    
    # 创建销售订单
    order = SalesOrder(**order_data.model_dump())
    
    db.add(order)
    await db.commit()
    await db.refresh(order)
    
    print(f"销售订单创建成功: {order.number}")
    return SalesOrderResponse.model_validate(order)

@router.get("/orders/{order_id}", response_model=SalesOrderResponse)
async def get_sales_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取销售订单详情"""
    result = await db.execute(
        select(SalesOrder).where(SalesOrder.id == order_id)
    )
    order = result.scalar_one_or_none()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="销售订单不存在"
        )
    
    return SalesOrderResponse.model_validate(order)

print("销售管理路由加载完成")