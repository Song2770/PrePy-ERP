from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from sqlalchemy.orm import Session
from typing import Any, List, Optional
from datetime import datetime

from ...models.user import User
from ...models.technical import (
    Product, Workstation,BOM,
    ProductionRoute, BOMItem
)
from ...config.database import get_db
from .auth import get_current_active_user
from pydantic import BaseModel

# 创建路由器
router = APIRouter(prefix="/technical", tags=["Technical"])

# ===========================
# Pydantic模型定义
# ===========================

# 工作中心模型
class WorkCenterBase(BaseModel):
    code: str
    name: str
    description: Optional[str] = None
    location: Optional[str] = None
    manager: Optional[str] = None
    is_active: bool = True

class WorkCenterCreate(WorkCenterBase):
    pass

class WorkCenterUpdate(WorkCenterBase):
    code: Optional[str] = None
    name: Optional[str] = None

class WorkCenterResponse(WorkCenterBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# 工作站模型
class WorkstationBase(BaseModel):
    code: str
    name: str
    description: Optional[str] = None
    work_center: Optional[int] = None
    capacity: Optional[float] = None
    capacity_uom: Optional[str] = None
    efficiency: Optional[float] = 1.0
    is_active: bool = True

class WorkstationCreate(WorkstationBase):
    pass

class WorkstationUpdate(WorkstationBase):
    code: Optional[str] = None
    name: Optional[str] = None

class WorkstationResponse(WorkstationBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# 产品规格模型
class ProductSpecificationBase(BaseModel):
    name: str
    value: str
    unit: Optional[str] = None
    description: Optional[str] = None

class ProductSpecificationCreate(ProductSpecificationBase):
    pass

class ProductSpecificationUpdate(ProductSpecificationBase):
    name: Optional[str] = None
    value: Optional[str] = None

class ProductSpecificationResponse(ProductSpecificationBase):
    id: int
    product_id: int
    
    class Config:
        from_attributes = True

# 产品模型
class ProductBase(BaseModel):
    code: str
    name: str
    description: Optional[str] = None
    category: str
    model: Optional[str] = None
    uom: str
    standard_cost: Optional[float] = None
    image_url: Optional[str] = None
    is_active: bool = True

class ProductCreate(ProductBase):
    specifications: Optional[List[ProductSpecificationCreate]] = None

class ProductUpdate(ProductBase):
    code: Optional[str] = None
    name: Optional[str] = None
    category: Optional[str] = None
    uom: Optional[str] = None

class ProductResponse(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime
    specifications: List[ProductSpecificationResponse] = []
    
    class Config:
        from_attributes = True

# 生产路线步骤模型
class RouteStepBase(BaseModel):
    sequence: int
    name: str
    work_center_id: Optional[int] = None
    workstation_id: Optional[int] = None
    standard_time: float = 0
    instructions: Optional[str] = None

class RouteStepCreate(RouteStepBase):
    pass

class RouteStepUpdate(RouteStepBase):
    sequence: Optional[int] = None
    name: Optional[str] = None
    standard_time: Optional[float] = None

class RouteStepResponse(RouteStepBase):
    id: int
    route_id: int
    work_center_name: Optional[str] = None
    workstation_name: Optional[str] = None
    
    class Config:
        from_attributes = True

# 生产路线模型
class ProductionRouteBase(BaseModel):
    code: str
    name: str
    product_id: int
    version: str = "1.0"
    description: Optional[str] = None
    status: str = "draft"  # draft, active, inactive
    total_time: float = 0
    notes: Optional[str] = None

class ProductionRouteCreate(ProductionRouteBase):
    steps: List[RouteStepCreate]

class ProductionRouteUpdate(ProductionRouteBase):
    code: Optional[str] = None
    name: Optional[str] = None
    product_id: Optional[int] = None
    version: Optional[str] = None
    status: Optional[str] = None

class ProductionRouteResponse(ProductionRouteBase):
    id: int
    product_name: str
    steps_count: int
    created_by: str
    created_at: datetime
    updated_at: datetime
    steps: List[RouteStepResponse] = []
    
    class Config:
        from_attributes = True

# BOM物料项模型
class BOMItemBase(BaseModel):
    material_id: int
    quantity: float
    uom: str
    position: Optional[str] = None
    is_key: bool = False
    remarks: Optional[str] = None

class BOMItemCreate(BOMItemBase):
    pass

class BOMItemUpdate(BOMItemBase):
    material_id: Optional[int] = None
    quantity: Optional[float] = None
    uom: Optional[str] = None

class BOMItemResponse(BOMItemBase):
    id: int
    bom_id: int
    material_code: str
    material_name: str
    material_type: str
    cost: Optional[float] = None
    
    class Config:
        from_attributes = True

# BOM模型
class BOMBase(BaseModel):
    product_id: int
    version: str = "1.0"
    type: str = "manufacturing"  # manufacturing, engineering, sales, template
    description: Optional[str] = None
    is_active: bool = True

class BOMCreate(BOMBase):
    items: List[BOMItemCreate]

class BOMUpdate(BOMBase):
    version: Optional[str] = None
    type: Optional[str] = None
    is_active: Optional[bool] = None

class BOMResponse(BOMBase):
    id: int
    product_code: str
    product_name: str
    created_by: str
    created_at: datetime
    updated_at: datetime
    items: List[BOMItemResponse] = []
    
    class Config:
        from_attributes = True

# ===========================
# 工作站API端点
# ===========================

@router.post("/workstations", response_model=WorkstationResponse, status_code=status.HTTP_201_CREATED)
async def create_workstation(
    workstation_data: WorkstationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    创建新工作站
    """
    # 检查编码是否已存在
    if db.query(Workstation).filter(Workstation.code == workstation_data.code).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="工作站编码已存在"
        )
    
    # 创建工作站
    workstation = Workstation(**workstation_data.dict())
    db.add(workstation)
    db.commit()
    db.refresh(workstation)
    
    return workstation

@router.get("/workstations", response_model=List[WorkstationResponse])
async def get_workstations(
    skip: int = 0,
    limit: int = 100,
    query: Optional[str] = None,
    work_center: Optional[int] = None,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    获取工作站列表
    """
    workstations_query = db.query(Workstation)
    
    # 应用过滤条件
    if query:
        search_term = f"%{query}%"
        workstations_query = workstations_query.filter(
            (Workstation.name.ilike(search_term)) | 
            (Workstation.code.ilike(search_term))
        )
    
    if work_center is not None:
        workstations_query = workstations_query.filter(Workstation.work_center == work_center)
    
    if is_active is not None:
        workstations_query = workstations_query.filter(Workstation.is_active == is_active)
    
    workstations = workstations_query.offset(skip).limit(limit).all()
    return workstations

@router.get("/workstations/{workstation_id}", response_model=WorkstationResponse)
async def get_workstation(
    workstation_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    获取工作站详情
    """
    workstation = db.query(Workstation).filter(Workstation.id == workstation_id).first()
    if not workstation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="工作站不存在"
        )
    
    return workstation

@router.put("/workstations/{workstation_id}", response_model=WorkstationResponse)
async def update_workstation(
    workstation_data: WorkstationUpdate,
    workstation_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    更新工作站
    """
    workstation = db.query(Workstation).filter(Workstation.id == workstation_id).first()
    if not workstation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="工作站不存在"
        )
    
    # 检查编码是否已存在
    if workstation_data.code and workstation_data.code != workstation.code:
        if db.query(Workstation).filter(Workstation.code == workstation_data.code).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="工作站编码已存在"
            )
    
    # 更新工作站
    for key, value in workstation_data.dict(exclude_unset=True).items():
        setattr(workstation, key, value)
    
    db.commit()
    db.refresh(workstation)
    
    return workstation

@router.delete("/workstations/{workstation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_workstation(
    workstation_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> None:
    """
    删除工作站
    """
    workstation = db.query(Workstation).filter(Workstation.id == workstation_id).first()
    if not workstation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="工作站不存在"
        )
    
    db.delete(workstation)
    db.commit()

# ===========================
# 产品API端点
# ===========================

@router.post("/products", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_data: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    创建新产品
    """
    # 检查编码是否已存在
    if db.query(Product).filter(Product.code == product_data.code).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="产品编码已存在"
        )
    
    # 提取规格数据
    specifications_data = None
    if hasattr(product_data, 'specifications'):
        specifications_data = product_data.specifications
        product_dict = product_data.dict(exclude={'specifications'})
    else:
        product_dict = product_data.dict()
    
    # 创建产品
    product = Product(**product_dict)
    db.add(product)
    db.commit()
    db.refresh(product)
    
    # 创建产品规格
    if specifications_data:
        for spec_data in specifications_data:
            spec = Product(**spec_data.dict(), product_id=product.id)
            db.add(spec)
        db.commit()
        db.refresh(product)
    
    return product

@router.get("/products", response_model=List[ProductResponse])
async def get_products(
    skip: int = 0,
    limit: int = 100,
    query: Optional[str] = None,
    category: Optional[str] = None,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    获取产品列表
    """
    products_query = db.query(Product)
    
    # 应用过滤条件
    if query:
        search_term = f"%{query}%"
        products_query = products_query.filter(
            (Product.name.ilike(search_term)) | 
            (Product.code.ilike(search_term)) |
            (Product.model.ilike(search_term))
        )
    
    if category:
        products_query = products_query.filter(Product.category == category)
    
    if is_active is not None:
        products_query = products_query.filter(Product.is_active == is_active)
    
    products = products_query.offset(skip).limit(limit).all()
    return products

@router.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    获取产品详情
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="产品不存在"
        )
    
    return product

# ===========================
# 生产路线API端点
# ===========================

@router.post("/routes", response_model=ProductionRouteResponse, status_code=status.HTTP_201_CREATED)
async def create_route(
    route_data: ProductionRouteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    创建新生产路线
    """
    # 检查产品是否存在
    product = db.query(Product).filter(Product.id == route_data.product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="产品不存在"
        )
    
    # 提取步骤数据
    steps_data = route_data.steps
    route_dict = route_data.dict(exclude={'steps'})
    
    # 计算总工时
    total_time = sum(step.standard_time for step in steps_data)
    route_dict['total_time'] = total_time
    
    # 添加创建者信息
    route_dict['created_by'] = current_user.username
    
    # 创建路线
    route = ProductionRoute(**route_dict)
    db.add(route)
    db.commit()
    db.refresh(route)
    
    # 创建路线步骤
    for step_data in steps_data:
        step = RouteStepResponse(**step_data.dict(), route_id=route.id)
        db.add(step)
    
    db.commit()
    db.refresh(route)
    
    return route

@router.get("/routes", response_model=List[ProductionRouteResponse])
async def get_routes(
    skip: int = 0,
    limit: int = 100,
    query: Optional[str] = None,
    product_id: Optional[int] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    获取生产路线列表
    """
    routes_query = db.query(ProductionRoute)
    
    # 应用过滤条件
    if query:
        search_term = f"%{query}%"
        routes_query = routes_query.filter(
            (ProductionRoute.name.ilike(search_term)) | 
            (ProductionRoute.code.ilike(search_term))
        )
    
    if product_id:
        routes_query = routes_query.filter(ProductionRoute.product_id == product_id)
    
    if status:
        routes_query = routes_query.filter(ProductionRoute.status == status)
    
    routes = routes_query.offset(skip).limit(limit).all()
    return routes

# ===========================
# BOM API端点
# ===========================

@router.post("/bom", response_model=BOMResponse, status_code=status.HTTP_201_CREATED)
async def create_bom(
    bom_data: BOMCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    创建新物料清单
    """
    # 检查产品是否存在
    product = db.query(Product).filter(Product.id == bom_data.product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="产品不存在"
        )
    
    # 提取物料项数据
    items_data = bom_data.items
    bom_dict = bom_data.dict(exclude={'items'})
    
    # 添加创建者信息和产品信息
    bom_dict['created_by'] = current_user.username
    bom_dict['name'] = product.name
    
    # 创建BOM
    bom = BOMCreate(**bom_dict)
    db.add(bom)
    db.commit()
    db.refresh(bom)
    
    # 创建BOM物料项
    for item_data in items_data:
        # 获取物料信息
        material = db.query(Product).filter(Product.id == item_data.material_id).first()
        if not material:
            # 如果物料不存在，可以回滚或跳过
            continue
        
        # 添加物料信息
        item = BOMItem(
            **item_data.dict(),
            bom_id=bom.id,
            material_code=material.code,
            material_name=material.name,
            material_type=material.category,
            cost=material.standard_cost
        )
        db.add(item)
    
    db.commit()
    db.refresh(bom)
    
    return bom

@router.get("/bom/product/{product_id}", response_model=BOMResponse)
async def get_product_bom(
    product_id: int = Path(..., gt=0),
    version: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    获取产品的物料清单
    """
    query = db.query(BOMBase).filter(
        BOM.product_id == product_id,
        BOM.is_active == True
    )
    
    if version:
        bom = query.filter(BOM.version == version).first()
    else:
        # 默认获取最新版本
        bom = query.order_by(BOM.version.desc()).first()
    
    if not bom:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="物料清单不存在"
        )
    
    return bom

@router.get("/bom/{bom_id}", response_model=BOMResponse)
async def get_bom_detail(
    bom_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    获取物料清单详情
    """
    bom = db.query(BOM).filter(BOM.id == bom_id).first()
    if not bom:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="物料清单不存在"
        )
    
    return bom 