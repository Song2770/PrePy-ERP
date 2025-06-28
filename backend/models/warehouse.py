from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Numeric, ForeignKey, Date
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class Warehouse(Base):
    """仓库模型"""
    __tablename__ = "warehouses"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, index=True, nullable=False, comment="仓库编码")
    name = Column(String(100), nullable=False, comment="仓库名称")
    
    # 基本信息
    warehouse_type = Column(String(20), default="普通仓库", comment="仓库类型(原料仓/半成品仓/成品仓/普通仓库)")
    location = Column(String(200), comment="仓库位置")
    manager_id = Column(Integer, ForeignKey("users.id"), comment="仓库管理员ID")
    
    # 状态字段
    is_active = Column(Boolean, default=True, comment="是否激活")
    
    # 时间字段
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # 备注
    description = Column(Text, comment="描述")
    
    # 关系
    manager = relationship("User")
    
    def __repr__(self):
        return f"<Warehouse(id={self.id}, code='{self.code}', name='{self.name}')>"

class Location(Base):
    """库位模型"""
    __tablename__ = "locations"
    
    id = Column(Integer, primary_key=True, index=True)
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=False, comment="仓库ID")
    code = Column(String(50), index=True, nullable=False, comment="库位编码")
    name = Column(String(100), comment="库位名称")
    
    # 位置信息
    zone = Column(String(20), comment="区域")
    aisle = Column(String(20), comment="通道")
    rack = Column(String(20), comment="货架")
    level = Column(String(20), comment="层")
    position = Column(String(20), comment="位置")
    
    # 状态字段
    is_active = Column(Boolean, default=True, comment="是否激活")
    
    # 时间字段
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # 关系
    warehouse = relationship("Warehouse", backref="locations")
    
    def __repr__(self):
        return f"<Location(id={self.id}, code='{self.code}', warehouse_id={self.warehouse_id})>"

class Inventory(Base):
    """库存模型"""
    __tablename__ = "inventory"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, comment="产品ID")
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=False, comment="仓库ID")
    location_id = Column(Integer, ForeignKey("locations.id"), comment="库位ID")
    
    # 数量信息
    quantity = Column(Numeric(10, 2), default=0, comment="库存数量")
    reserved_quantity = Column(Numeric(10, 2), default=0, comment="预留数量")
    available_quantity = Column(Numeric(10, 2), default=0, comment="可用数量")
    
    # 成本信息
    unit_cost = Column(Numeric(15, 4), default=0, comment="单位成本")
    total_cost = Column(Numeric(15, 2), default=0, comment="总成本")
    
    # 批次信息
    batch_number = Column(String(50), comment="批次号")
    production_date = Column(Date, comment="生产日期")
    expiry_date = Column(Date, comment="过期日期")
    
    # 时间字段
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # 关系
    product = relationship("Product")
    warehouse = relationship("Warehouse")
    location = relationship("Location")
    
    def __repr__(self):
        return f"<Inventory(id={self.id}, product_id={self.product_id}, warehouse_id={self.warehouse_id}, quantity={self.quantity})>"

class StockMovement(Base):
    """库存移动记录模型"""
    __tablename__ = "stock_movements"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, comment="产品ID")
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=False, comment="仓库ID")
    location_id = Column(Integer, ForeignKey("locations.id"), comment="库位ID")
    
    # 移动信息
    movement_type = Column(String(20), nullable=False, comment="移动类型(入库/出库/调拨/盘点)")
    reference_type = Column(String(50), comment="关联单据类型")
    reference_id = Column(Integer, comment="关联单据ID")
    reference_number = Column(String(50), comment="关联单据号")
    
    # 数量信息
    quantity = Column(Numeric(10, 2), nullable=False, comment="移动数量")
    unit_cost = Column(Numeric(15, 4), comment="单位成本")
    
    # 批次信息
    batch_number = Column(String(50), comment="批次号")
    
    # 时间字段
    movement_date = Column(DateTime, nullable=False, comment="移动时间")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    
    # 备注
    notes = Column(Text, comment="备注")
    
    # 关系
    product = relationship("Product")
    warehouse = relationship("Warehouse")
    location = relationship("Location")
    
    def __repr__(self):
        return f"<StockMovement(id={self.id}, product_id={self.product_id}, movement_type='{self.movement_type}', quantity={self.quantity})>"

class StockTaking(Base):
    """盘点单模型"""
    __tablename__ = "stock_takings"
    
    id = Column(Integer, primary_key=True, index=True)
    number = Column(String(50), unique=True, index=True, nullable=False, comment="盘点单号")
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=False, comment="仓库ID")
    
    # 基本信息
    taking_date = Column(Date, nullable=False, comment="盘点日期")
    taking_type = Column(String(20), default="全盘", comment="盘点类型(全盘/抽盘/循环盘点)")
    
    # 状态
    status = Column(String(20), default="计划中", comment="状态(计划中/盘点中/已完成/已取消)")
    
    # 时间字段
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # 备注
    notes = Column(Text, comment="备注")
    
    # 关系
    warehouse = relationship("Warehouse", backref="stock_takings")
    
    def __repr__(self):
        return f"<StockTaking(id={self.id}, number='{self.number}', warehouse_id={self.warehouse_id})>"

class StockTakingLine(Base):
    """盘点单明细模型"""
    __tablename__ = "stock_taking_lines"
    
    id = Column(Integer, primary_key=True, index=True)
    taking_id = Column(Integer, ForeignKey("stock_takings.id"), nullable=False, comment="盘点单ID")
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, comment="产品ID")
    location_id = Column(Integer, ForeignKey("locations.id"), comment="库位ID")
    
    # 数量信息
    book_quantity = Column(Numeric(10, 2), default=0, comment="账面数量")
    actual_quantity = Column(Numeric(10, 2), comment="实盘数量")
    difference_quantity = Column(Numeric(10, 2), default=0, comment="差异数量")
    
    # 批次信息
    batch_number = Column(String(50), comment="批次号")
    
    # 盘点信息
    counter_id = Column(Integer, ForeignKey("users.id"), comment="盘点员ID")
    count_date = Column(DateTime, comment="盘点时间")
    
    # 时间字段
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # 备注
    notes = Column(Text, comment="备注")
    
    # 关系
    taking = relationship("StockTaking", backref="lines")
    product = relationship("Product")
    location = relationship("Location")
    counter = relationship("User")
    
    def __repr__(self):
        return f"<StockTakingLine(id={self.id}, taking_id={self.taking_id}, product_id={self.product_id})>"