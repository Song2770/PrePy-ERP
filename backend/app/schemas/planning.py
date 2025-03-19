from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date, datetime

from ..models.planning import PlanStatus

# 生产计划项目模型
class ProductionPlanItemBase(BaseModel):
    product_id: int
    order_id: Optional[int] = None
    order_item_id: Optional[int] = None
    quantity: float
    unit: Optional[str] = None
    planned_start_date: date
    planned_end_date: date
    status: PlanStatus = PlanStatus.DRAFT
    notes: Optional[str] = None

class ProductionPlanItemCreate(ProductionPlanItemBase):
    pass

class ProductionPlanItemUpdate(BaseModel):
    product_id: Optional[int] = None
    order_id: Optional[int] = None
    order_item_id: Optional[int] = None
    quantity: Optional[float] = None
    unit: Optional[str] = None
    planned_start_date: Optional[date] = None
    planned_end_date: Optional[date] = None
    actual_start_date: Optional[date] = None
    actual_end_date: Optional[date] = None
    status: Optional[PlanStatus] = None
    notes: Optional[str] = None

class ProductionPlanItemResponse(ProductionPlanItemBase):
    id: int
    plan_id: int
    actual_start_date: Optional[date] = None
    actual_end_date: Optional[date] = None
    
    class Config:
        orm_mode = True

# 生产计划模型
class ProductionPlanBase(BaseModel):
    name: str
    description: Optional[str] = None
    planned_start_date: date
    planned_end_date: date

class ProductionPlanCreate(ProductionPlanBase):
    pass

class ProductionPlanUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[PlanStatus] = None
    planned_start_date: Optional[date] = None
    planned_end_date: Optional[date] = None
    actual_start_date: Optional[date] = None
    actual_end_date: Optional[date] = None

class ProductionPlanResponse(ProductionPlanBase):
    id: int
    plan_number: str
    status: PlanStatus
    actual_start_date: Optional[date] = None
    actual_end_date: Optional[date] = None
    created_by_id: int
    created_at: datetime
    updated_at: datetime
    items: List[ProductionPlanItemResponse] = []
    
    class Config:
        orm_mode = True

# MRP项目模型
class MRPItemBase(BaseModel):
    material_id: int
    required_date: date
    required_quantity: float
    available_quantity: float = 0.0
    on_order_quantity: float = 0.0
    net_requirement: float
    notes: Optional[str] = None

class MRPItemCreate(MRPItemBase):
    pass

class MRPItemResponse(MRPItemBase):
    id: int
    mrp_id: int
    
    class Config:
        orm_mode = True

# MRP模型
class MRPBase(BaseModel):
    name: str
    description: Optional[str] = None
    planning_horizon: int = Field(..., gt=0, description="计划周期(天)")

class MRPCreate(MRPBase):
    pass

class MRPUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[PlanStatus] = None
    planning_horizon: Optional[int] = Field(None, gt=0)

class MRPResponse(MRPBase):
    id: int
    mrp_number: str
    status: PlanStatus
    created_by_id: int
    created_at: datetime
    updated_at: datetime
    items: List[MRPItemResponse] = []
    
    class Config:
        orm_mode = True 