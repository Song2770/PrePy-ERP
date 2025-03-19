from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import date

from ..models.planning import ProductionPlan, ProductionPlanItem, MaterialRequirementPlan, MRPItem, PlanStatus
from ..schemas.planning import (
    ProductionPlanCreate, ProductionPlanUpdate, ProductionPlanResponse,
    ProductionPlanItemCreate, ProductionPlanItemUpdate, ProductionPlanItemResponse,
    MRPCreate, MRPUpdate, MRPResponse,
    MRPItemCreate, MRPItemResponse
)
from ..config.database import get_db
from backend.app.api.v1.auth import get_current_user
from ..models.user import User
from ..utils.pagination import paginate, PaginatedResponse

router = APIRouter(prefix="/planning", tags=["planning"])

# 生产计划相关路由
@router.post("/production-plans", response_model=ProductionPlanResponse, status_code=status.HTTP_201_CREATED)
def create_production_plan(
    plan: ProductionPlanCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建生产计划"""
    # 生成计划编号
    from datetime import datetime
    plan_number = f"PP-{datetime.now().strftime('%Y%m%d')}-{datetime.now().strftime('%H%M%S')}"
    
    db_plan = ProductionPlan(
        plan_number=plan_number,
        name=plan.name,
        description=plan.description,
        status=PlanStatus.DRAFT,
        planned_start_date=plan.planned_start_date,
        planned_end_date=plan.planned_end_date,
        created_by_id=current_user.id
    )
    
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)
    
    return db_plan

@router.get("/production-plans", response_model=PaginatedResponse[ProductionPlanResponse])
def list_production_plans(
    status: Optional[PlanStatus] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取生产计划列表"""
    query = db.query(ProductionPlan)
    
    # 过滤条件
    if status:
        query = query.filter(ProductionPlan.status == status)
    if start_date:
        query = query.filter(ProductionPlan.planned_start_date >= start_date)
    if end_date:
        query = query.filter(ProductionPlan.planned_end_date <= end_date)
    
    # 排序
    query = query.order_by(ProductionPlan.created_at.desc())
    
    return paginate(query, page, page_size)

@router.get("/production-plans/{plan_id}", response_model=ProductionPlanResponse)
def get_production_plan(
    plan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取生产计划详情"""
    db_plan = db.query(ProductionPlan).filter(ProductionPlan.id == plan_id).first()
    if not db_plan:
        raise HTTPException(status_code=404, detail="生产计划不存在")
    
    return db_plan

@router.put("/production-plans/{plan_id}", response_model=ProductionPlanResponse)
def update_production_plan(
    plan_id: int,
    plan: ProductionPlanUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新生产计划"""
    db_plan = db.query(ProductionPlan).filter(ProductionPlan.id == plan_id).first()
    if not db_plan:
        raise HTTPException(status_code=404, detail="生产计划不存在")
    
    # 更新字段
    for key, value in plan.dict(exclude_unset=True).items():
        setattr(db_plan, key, value)
    
    db.commit()
    db.refresh(db_plan)
    
    return db_plan

@router.delete("/production-plans/{plan_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_production_plan(
    plan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """删除生产计划"""
    db_plan = db.query(ProductionPlan).filter(ProductionPlan.id == plan_id).first()
    if not db_plan:
        raise HTTPException(status_code=404, detail="生产计划不存在")
    
    db.delete(db_plan)
    db.commit()
    
    return None

# 生产计划项目相关路由
@router.post("/production-plans/{plan_id}/items", response_model=ProductionPlanItemResponse)
def add_production_plan_item(
    plan_id: int,
    item: ProductionPlanItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """添加生产计划项目"""
    db_plan = db.query(ProductionPlan).filter(ProductionPlan.id == plan_id).first()
    if not db_plan:
        raise HTTPException(status_code=404, detail="生产计划不存在")
    
    db_item = ProductionPlanItem(
        plan_id=plan_id,
        **item.dict()
    )
    
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    
    return db_item

@router.put("/production-plan-items/{item_id}", response_model=ProductionPlanItemResponse)
def update_production_plan_item(
    item_id: int,
    item: ProductionPlanItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新生产计划项目"""
    db_item = db.query(ProductionPlanItem).filter(ProductionPlanItem.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="生产计划项目不存在")
    
    # 更新字段
    for key, value in item.dict(exclude_unset=True).items():
        setattr(db_item, key, value)
    
    db.commit()
    db.refresh(db_item)
    
    return db_item

@router.delete("/production-plan-items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_production_plan_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """删除生产计划项目"""
    db_item = db.query(ProductionPlanItem).filter(ProductionPlanItem.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="生产计划项目不存在")
    
    db.delete(db_item)
    db.commit()
    
    return None

# 物料需求计划相关路由
@router.post("/mrp", response_model=MRPResponse)
def create_mrp(
    mrp: MRPCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建物料需求计划"""
    # 生成计划编号
    from datetime import datetime
    mrp_number = f"MRP-{datetime.now().strftime('%Y%m%d')}-{datetime.now().strftime('%H%M%S')}"
    
    db_mrp = MaterialRequirementPlan(
        mrp_number=mrp_number,
        name=mrp.name,
        description=mrp.description,
        status=PlanStatus.DRAFT,
        planning_horizon=mrp.planning_horizon,
        created_by_id=current_user.id
    )
    
    db.add(db_mrp)
    db.commit()
    db.refresh(db_mrp)
    
    return db_mrp

@router.get("/mrp", response_model=PaginatedResponse[MRPResponse])
def list_mrp(
    status: Optional[PlanStatus] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取物料需求计划列表"""
    query = db.query(MaterialRequirementPlan)
    
    # 过滤条件
    if status:
        query = query.filter(MaterialRequirementPlan.status == status)
    
    # 排序
    query = query.order_by(MaterialRequirementPlan.created_at.desc())
    
    return paginate(query, page, page_size)

@router.get("/mrp/{mrp_id}", response_model=MRPResponse)
def get_mrp(
    mrp_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取物料需求计划详情"""
    db_mrp = db.query(MaterialRequirementPlan).filter(MaterialRequirementPlan.id == mrp_id).first()
    if not db_mrp:
        raise HTTPException(status_code=404, detail="物料需求计划不存在")
    
    return db_mrp

@router.put("/mrp/{mrp_id}", response_model=MRPResponse)
def update_mrp(
    mrp_id: int,
    mrp: MRPUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新物料需求计划"""
    db_mrp = db.query(MaterialRequirementPlan).filter(MaterialRequirementPlan.id == mrp_id).first()
    if not db_mrp:
        raise HTTPException(status_code=404, detail="物料需求计划不存在")
    
    # 更新字段
    for key, value in mrp.dict(exclude_unset=True).items():
        setattr(db_mrp, key, value)
    
    db.commit()
    db.refresh(db_mrp)
    
    return db_mrp

@router.post("/mrp/{mrp_id}/run")
def run_mrp(
    mrp_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """运行MRP计算"""
    db_mrp = db.query(MaterialRequirementPlan).filter(MaterialRequirementPlan.id == mrp_id).first()
    if not db_mrp:
        raise HTTPException(status_code=404, detail="物料需求计划不存在")
    
    # TODO: 实现MRP计算逻辑
    
    # 更新状态
    db_mrp.status = PlanStatus.CONFIRMED
    db.commit()
    
    return {"message": "MRP计算完成"}

@router.delete("/mrp/{mrp_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_mrp(
    mrp_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """删除物料需求计划"""
    db_mrp = db.query(MaterialRequirementPlan).filter(MaterialRequirementPlan.id == mrp_id).first()
    if not db_mrp:
        raise HTTPException(status_code=404, detail="物料需求计划不存在")
    
    db.delete(db_mrp)
    db.commit()
    
    return None 