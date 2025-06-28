from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import List, Optional
from decimal import Decimal
from datetime import datetime
from database import get_db
from models.warehouse import Inventory, StockMovement
from models.user import User
from utils.auth import verify_token

print("正在加载仓库管理路由...")

router = APIRouter()
security = HTTPBearer()

class InventoryResponse(BaseModel):
    id: int
    product_id: int
    warehouse_id: int
    location_id: Optional[int]
    quantity_on_hand: Decimal
    quantity_reserved: Decimal
    quantity_available: Decimal
    unit_cost: Optional[Decimal]
    batch_number: Optional[str]
    expiry_date: Optional[datetime]
    created_at: str
    
    class Config:
        from_attributes = True

class StockMovementCreate(BaseModel):
    product_id: int
    warehouse_id: int
    location_id: Optional[int] = None
    movement_type: str  # 入库/出库
    quantity: Decimal
    unit_cost: Optional[Decimal] = None
    reference_type: Optional[str] = None
    reference_id: Optional[int] = None
    notes: Optional[str] = None

class StockMovementResponse(BaseModel):
    id: int
    product_id: int
    warehouse_id: int
    location_id: Optional[int]
    movement_type: str
    quantity: Decimal
    unit_cost: Optional[Decimal]
    reference_type: Optional[str]
    reference_id: Optional[int]
    notes: Optional[str]
    movement_date: datetime
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

@router.get("/inventory", response_model=List[InventoryResponse])
async def get_inventory(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取库存列表"""
    print(f"获取库存列表，跳过: {skip}, 限制: {limit}")
    
    result = await db.execute(
        select(Inventory).offset(skip).limit(limit)
    )
    inventory = result.scalars().all()
    
    return [InventoryResponse.model_validate(inv) for inv in inventory]

@router.get("/stock-movements", response_model=List[StockMovementResponse])
async def get_stock_movements(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取库存移动记录"""
    print(f"获取库存移动记录，跳过: {skip}, 限制: {limit}")
    
    result = await db.execute(
        select(StockMovement).offset(skip).limit(limit)
    )
    movements = result.scalars().all()
    
    return [StockMovementResponse.model_validate(mov) for mov in movements]

@router.post("/stock-movements", response_model=StockMovementResponse)
async def create_stock_movement(
    movement_data: StockMovementCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """创建库存移动记录"""
    print(f"创建库存移动记录: {movement_data.movement_type}")
    
    # 创建库存移动记录
    movement = StockMovement(
        **movement_data.model_dump(),
        movement_date=datetime.now()
    )
    
    db.add(movement)
    await db.commit()
    await db.refresh(movement)
    
    print(f"库存移动记录创建成功: {movement.movement_type}")
    return StockMovementResponse.model_validate(movement)

print("仓库管理路由加载完成")