from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import List, Optional
from decimal import Decimal
from database import get_db
from models.product import Product, ProductCategory
from models.user import User
from utils.auth import verify_token

print("正在加载产品管理路由...")

router = APIRouter()
security = HTTPBearer()

class ProductCreate(BaseModel):
    code: str
    name: str
    specification: Optional[str] = None
    category_id: Optional[int] = None
    unit: str = "个"
    standard_cost: Optional[Decimal] = 0
    selling_price: Optional[Decimal] = 0
    product_type: str = "成品"
    is_active: bool = True
    is_sellable: bool = True
    is_purchasable: bool = False
    is_manufacturable: bool = False

class ProductResponse(BaseModel):
    id: int
    code: str
    name: str
    specification: Optional[str]
    category_id: Optional[int]
    unit: str
    standard_cost: Optional[Decimal]
    selling_price: Optional[Decimal]
    product_type: str
    is_active: bool
    is_sellable: bool
    is_purchasable: bool
    is_manufacturable: bool
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

@router.get("/", response_model=List[ProductResponse])
async def get_products(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取产品列表"""
    print(f"获取产品列表，跳过: {skip}, 限制: {limit}")
    
    result = await db.execute(
        select(Product).offset(skip).limit(limit)
    )
    products = result.scalars().all()
    
    return [ProductResponse.model_validate(product) for product in products]

@router.post("/", response_model=ProductResponse)
async def create_product(
    product_data: ProductCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """创建产品"""
    print(f"创建产品: {product_data.name}")
    
    # 检查产品编码是否已存在
    result = await db.execute(
        select(Product).where(Product.code == product_data.code)
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="产品编码已存在"
        )
    
    # 创建产品
    product = Product(**product_data.model_dump())
    
    db.add(product)
    await db.commit()
    await db.refresh(product)
    
    print(f"产品创建成功: {product.name}")
    return ProductResponse.model_validate(product)

@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取产品详情"""
    result = await db.execute(
        select(Product).where(Product.id == product_id)
    )
    product = result.scalar_one_or_none()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="产品不存在"
        )
    
    return ProductResponse.model_validate(product)

print("产品管理路由加载完成")