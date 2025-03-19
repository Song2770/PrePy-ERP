from sqlalchemy import (
    Boolean, Column, ForeignKey, Integer, String, 
    DateTime, Text, Enum, Float, Date, Table, UniqueConstraint
)
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from ..config.database import Base

class PlanStatus(str, enum.Enum):
    """计划状态枚举"""
    DRAFT = "draft"
    CONFIRMED = "confirmed"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class ProductionPlan(Base):
    """生产计划模型"""
    __tablename__ = "production_plans"

    id = Column(Integer, primary_key=True, index=True)
    plan_number = Column(String, unique=True, index=True)
    name = Column(String, index=True)
    description = Column(Text, nullable=True)
    status = Column(Enum(PlanStatus), default=PlanStatus.DRAFT)
    planned_start_date = Column(Date)
    planned_end_date = Column(Date)
    actual_start_date = Column(Date, nullable=True)
    actual_end_date = Column(Date, nullable=True)
    created_by_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关联关系
    created_by = relationship("User", back_populates="production_plans")
    items = relationship("ProductionPlanItem", back_populates="plan", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<ProductionPlan {self.plan_number}>"

class ProductionPlanItem(Base):
    """生产计划项目模型"""
    __tablename__ = "production_plan_items"

    id = Column(Integer, primary_key=True, index=True)
    plan_id = Column(Integer, ForeignKey("production_plans.id", ondelete="CASCADE"))
    product_id = Column(Integer, ForeignKey("products.id"))
    order_id = Column(Integer, ForeignKey("sales_orders.id"), nullable=True)
    order_item_id = Column(Integer, ForeignKey("sales_order_items.id"), nullable=True)
    quantity = Column(Float)
    unit = Column(String, nullable=True)
    planned_start_date = Column(Date)
    planned_end_date = Column(Date)
    actual_start_date = Column(Date, nullable=True)
    actual_end_date = Column(Date, nullable=True)
    notes = Column(Text, nullable=True)
    status = Column(Enum(PlanStatus), default=PlanStatus.DRAFT)

    # 关联关系
    plan = relationship("ProductionPlan", back_populates="items")
    product = relationship("Product")
    order = relationship("SalesOrder")
    order_item = relationship("SalesOrderItem")

    def __repr__(self):
        return f"<ProductionPlanItem {self.id}>"

class MaterialRequirementPlan(Base):
    """物料需求计划模型"""
    __tablename__ = "material_requirement_plans"

    id = Column(Integer, primary_key=True, index=True)
    mrp_number = Column(String, unique=True, index=True)
    name = Column(String, index=True)
    description = Column(Text, nullable=True)
    status = Column(Enum(PlanStatus), default=PlanStatus.DRAFT)
    planning_horizon = Column(Integer)  # 计划周期(天)
    created_by_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关联关系
    created_by = relationship("User", back_populates="mrp_plans")
    items = relationship("MRPItem", back_populates="mrp", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<MaterialRequirementPlan {self.mrp_number}>"

class MRPItem(Base):
    """物料需求计划项目模型"""
    __tablename__ = "mrp_items"

    id = Column(Integer, primary_key=True, index=True)
    mrp_id = Column(Integer, ForeignKey("material_requirement_plans.id", ondelete="CASCADE"))
    material_id = Column(Integer, ForeignKey("products.id"))
    required_date = Column(Date)
    required_quantity = Column(Float)
    available_quantity = Column(Float, default=0.0)
    on_order_quantity = Column(Float, default=0.0)
    net_requirement = Column(Float)
    notes = Column(Text, nullable=True)

    # 关联关系
    mrp = relationship("MaterialRequirementPlan", back_populates="items")
    material = relationship("Product")

    def __repr__(self):
        return f"<MRPItem {self.id}>" 