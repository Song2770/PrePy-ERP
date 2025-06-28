from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from database import get_db
from models.customer import Customer
from models.user import User
from utils.auth import verify_token

print("正在加载客户管理路由...")

router = APIRouter()
security = HTTPBearer()

class CustomerCreate(BaseModel):
    code: str
    name: str
    short_name: Optional[str] = None
    contact_person: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    city: Optional[str] = None
    province: Optional[str] = None
    customer_type: str = "普通客户"
    level: str = "C"
    is_active: bool = True

class CustomerResponse(BaseModel):
    id: int
    code: str
    name: str
    short_name: Optional[str]
    contact_person: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    address: Optional[str]
    city: Optional[str]
    province: Optional[str]
    customer_type: str
    level: str
    is_active: bool
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

@router.get("/", response_model=List[CustomerResponse])
async def get_customers(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取客户列表"""
    print(f"获取客户列表，跳过: {skip}, 限制: {limit}")
    
    result = await db.execute(
        select(Customer).offset(skip).limit(limit)
    )
    customers = result.scalars().all()
    
    return [CustomerResponse.model_validate(customer) for customer in customers]

@router.post("/", response_model=CustomerResponse)
async def create_customer(
    customer_data: CustomerCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """创建客户"""
    print(f"创建客户: {customer_data.name}")
    
    # 检查客户编码是否已存在
    result = await db.execute(
        select(Customer).where(Customer.code == customer_data.code)
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="客户编码已存在"
        )
    
    # 创建客户
    customer = Customer(**customer_data.model_dump())
    
    db.add(customer)
    await db.commit()
    await db.refresh(customer)
    
    print(f"客户创建成功: {customer.name}")
    return CustomerResponse.model_validate(customer)

@router.get("/{customer_id}", response_model=CustomerResponse)
async def get_customer(
    customer_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取客户详情"""
    result = await db.execute(
        select(Customer).where(Customer.id == customer_id)
    )
    customer = result.scalar_one_or_none()
    
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="客户不存在"
        )
    
    return CustomerResponse.model_validate(customer)

@router.put("/{customer_id}", response_model=CustomerResponse)
async def update_customer(
    customer_id: int,
    customer_data: CustomerCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """更新客户"""
    print(f"更新客户: {customer_id}")
    
    result = await db.execute(
        select(Customer).where(Customer.id == customer_id)
    )
    customer = result.scalar_one_or_none()
    
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="客户不存在"
        )
    
    # 更新客户信息
    update_data = customer_data.model_dump()
    for field, value in update_data.items():
        setattr(customer, field, value)
    
    await db.commit()
    await db.refresh(customer)
    
    print(f"客户更新成功: {customer.name}")
    return CustomerResponse.model_validate(customer)

@router.delete("/{customer_id}")
async def delete_customer(
    customer_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """删除客户"""
    print(f"删除客户: {customer_id}")
    
    result = await db.execute(
        select(Customer).where(Customer.id == customer_id)
    )
    customer = result.scalar_one_or_none()
    
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="客户不存在"
        )
    
    await db.delete(customer)
    await db.commit()
    
    print(f"客户删除成功: {customer.name}")
    return {"message": "客户删除成功"}

print("客户管理路由加载完成")