from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Numeric, ForeignKey, Date
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class WorkOrder(Base):
    """工单模型"""
    __tablename__ = "work_orders"
    
    id = Column(Integer, primary_key=True, index=True)
    number = Column(String(50), unique=True, index=True, nullable=False, comment="工单号")
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, comment="产品ID")
    sales_order_line_id = Column(Integer, ForeignKey("sales_order_lines.id"), comment="销售订单明细ID")
    bom_id = Column(Integer, ForeignKey("boms.id"), comment="BOM ID")
    
    # 数量信息
    planned_quantity = Column(Numeric(10, 2), nullable=False, comment="计划数量")
    produced_quantity = Column(Numeric(10, 2), default=0, comment="已生产数量")
    scrap_quantity = Column(Numeric(10, 2), default=0, comment="报废数量")
    
    # 时间计划
    planned_start_date = Column(Date, comment="计划开始日期")
    planned_end_date = Column(Date, comment="计划完成日期")
    actual_start_date = Column(Date, comment="实际开始日期")
    actual_end_date = Column(Date, comment="实际完成日期")
    
    # 优先级
    priority = Column(String(20), default="普通", comment="优先级(紧急/高/普通/低)")
    
    # 状态
    status = Column(String(20), default="计划中", comment="状态(计划中/已下达/生产中/已完成/已取消)")
    
    # 时间字段
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # 备注
    notes = Column(Text, comment="备注")
    
    # 关系
    product = relationship("Product", backref="work_orders")
    sales_order_line = relationship("SalesOrderLine")
    bom = relationship("BOM")
    
    def __repr__(self):
        return f"<WorkOrder(id={self.id}, number='{self.number}', product_id={self.product_id})>"

class WorkOrderOperation(Base):
    """工单工序模型"""
    __tablename__ = "work_order_operations"
    
    id = Column(Integer, primary_key=True, index=True)
    work_order_id = Column(Integer, ForeignKey("work_orders.id"), nullable=False, comment="工单ID")
    operation_id = Column(Integer, ForeignKey("operations.id"), nullable=False, comment="工序ID")
    sequence = Column(Integer, nullable=False, comment="工序序号")
    
    # 时间信息
    planned_start_time = Column(DateTime, comment="计划开始时间")
    planned_end_time = Column(DateTime, comment="计划结束时间")
    actual_start_time = Column(DateTime, comment="实际开始时间")
    actual_end_time = Column(DateTime, comment="实际结束时间")
    
    # 数量信息
    planned_quantity = Column(Numeric(10, 2), nullable=False, comment="计划数量")
    completed_quantity = Column(Numeric(10, 2), default=0, comment="完成数量")
    scrap_quantity = Column(Numeric(10, 2), default=0, comment="报废数量")
    
    # 状态
    status = Column(String(20), default="等待", comment="状态(等待/进行中/已完成/暂停)")
    
    # 时间字段
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # 备注
    notes = Column(Text, comment="备注")
    
    # 关系
    work_order = relationship("WorkOrder", backref="operations")
    operation = relationship("Operation")
    
    def __repr__(self):
        return f"<WorkOrderOperation(id={self.id}, work_order_id={self.work_order_id}, operation_id={self.operation_id})>"

class Operation(Base):
    """工序模型"""
    __tablename__ = "operations"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, index=True, nullable=False, comment="工序编码")
    name = Column(String(100), nullable=False, comment="工序名称")
    
    # 工序信息
    work_center_id = Column(Integer, ForeignKey("work_centers.id"), comment="工作中心ID")
    setup_time = Column(Numeric(8, 2), default=0, comment="准备时间(分钟)")
    cycle_time = Column(Numeric(8, 2), default=0, comment="单件时间(分钟)")
    
    # 状态字段
    is_active = Column(Boolean, default=True, comment="是否激活")
    
    # 时间字段
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # 备注
    description = Column(Text, comment="工序描述")
    
    # 关系
    work_center = relationship("WorkCenter", backref="operations")
    
    def __repr__(self):
        return f"<Operation(id={self.id}, code='{self.code}', name='{self.name}')>"

class WorkCenter(Base):
    """工作中心模型"""
    __tablename__ = "work_centers"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, index=True, nullable=False, comment="工作中心编码")
    name = Column(String(100), nullable=False, comment="工作中心名称")
    
    # 产能信息
    capacity_per_day = Column(Numeric(8, 2), default=8, comment="日产能(小时)")
    efficiency = Column(Numeric(5, 2), default=100, comment="效率(%)")
    
    # 成本信息
    hourly_rate = Column(Numeric(10, 2), default=0, comment="小时费率")
    
    # 状态字段
    is_active = Column(Boolean, default=True, comment="是否激活")
    
    # 时间字段
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # 备注
    description = Column(Text, comment="描述")
    location = Column(String(100), comment="位置")
    
    def __repr__(self):
        return f"<WorkCenter(id={self.id}, code='{self.code}', name='{self.name}')>"

class ProductionRecord(Base):
    """生产记录模型"""
    __tablename__ = "production_records"
    
    id = Column(Integer, primary_key=True, index=True)
    work_order_operation_id = Column(Integer, ForeignKey("work_order_operations.id"), nullable=False, comment="工单工序ID")
    operator_id = Column(Integer, ForeignKey("users.id"), comment="操作员ID")
    
    # 时间信息
    start_time = Column(DateTime, nullable=False, comment="开始时间")
    end_time = Column(DateTime, comment="结束时间")
    duration = Column(Numeric(8, 2), comment="工时(小时)")
    
    # 数量信息
    good_quantity = Column(Numeric(10, 2), default=0, comment="合格数量")
    scrap_quantity = Column(Numeric(10, 2), default=0, comment="报废数量")
    rework_quantity = Column(Numeric(10, 2), default=0, comment="返工数量")
    
    # 时间字段
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # 备注
    notes = Column(Text, comment="备注")
    
    # 关系
    work_order_operation = relationship("WorkOrderOperation", backref="records")
    operator = relationship("User")
    
    def __repr__(self):
        return f"<ProductionRecord(id={self.id}, work_order_operation_id={self.work_order_operation_id})>"