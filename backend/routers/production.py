from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import List, Optional
from decimal import Decimal
from datetime import date
from database import get_db
from models.production import WorkOrder
from models.user import User
from utils.auth import verify_token

print("正在加载生产管理路由...")

router = APIRouter()
security = HTTPBearer()

class WorkOrderCreate(BaseModel):
    number: str
    product_id: int
    planned_quantity: Decimal
    planned_start_date: Optional[date] = None
    planned_end_date: Optional[date] = None
    priority: str = "普通"
    status: str = "计划中"

class WorkOrderResponse(BaseModel):
    id: int
    number: str
    product_id: int
    planned_quantity: Decimal
    produced_quantity: Decimal
    planned_start_date: Optional[date]
    planned_end_date: Optional[date]
    priority: str
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

@router.get("/work-orders", response_model=List[WorkOrderResponse])
async def get_work_orders(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取工单列表"""
    print(f"获取工单列表，跳过: {skip}, 限制: {limit}")
    
    result = await db.execute(
        select(WorkOrder).offset(skip).limit(limit)
    )
    work_orders = result.scalars().all()
    
    return [WorkOrderResponse.model_validate(wo) for wo in work_orders]

@router.post("/work-orders", response_model=WorkOrderResponse)
async def create_work_order(
    work_order_data: WorkOrderCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """创建工单"""
    print(f"创建工单: {work_order_data.number}")
    
    # 检查工单号是否已存在
    result = await db.execute(
        select(WorkOrder).where(WorkOrder.number == work_order_data.number)
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="工单号已存在"
        )
    
    # 创建工单
    work_order = WorkOrder(**work_order_data.model_dump())
    
    db.add(work_order)
    await db.commit()
    await db.refresh(work_order)
    
    print(f"工单创建成功: {work_order.number}")
    return WorkOrderResponse.model_validate(work_order)

print("生产管理路由加载完成")