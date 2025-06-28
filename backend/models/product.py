from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Numeric, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class ProductCategory(Base):
    """产品分类模型"""
    __tablename__ = "product_categories"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, index=True, nullable=False, comment="分类编码")
    name = Column(String(100), nullable=False, comment="分类名称")
    parent_id = Column(Integer, ForeignKey("product_categories.id"), comment="父分类ID")
    
    # 状态字段
    is_active = Column(Boolean, default=True, comment="是否激活")
    
    # 时间字段
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # 备注
    description = Column(Text, comment="描述")
    
    # 关系
    parent = relationship("ProductCategory", remote_side=[id], backref="children")
    
    def __repr__(self):
        return f"<ProductCategory(id={self.id}, code='{self.code}', name='{self.name}')>"

class Product(Base):
    """产品模型"""
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, index=True, nullable=False, comment="产品编码")
    name = Column(String(100), nullable=False, comment="产品名称")
    specification = Column(String(200), comment="规格型号")
    category_id = Column(Integer, ForeignKey("product_categories.id"), comment="分类ID")
    
    # 基本信息
    unit = Column(String(20), default="个", comment="计量单位")
    weight = Column(Numeric(10, 3), comment="重量(kg)")
    volume = Column(Numeric(10, 3), comment="体积(m³)")
    color = Column(String(50), comment="颜色")
    material = Column(String(100), comment="材质")
    
    # 价格信息
    standard_cost = Column(Numeric(15, 2), default=0, comment="标准成本")
    selling_price = Column(Numeric(15, 2), default=0, comment="销售价格")
    
    # 库存信息
    min_stock = Column(Numeric(10, 2), default=0, comment="最小库存")
    max_stock = Column(Numeric(10, 2), default=0, comment="最大库存")
    safety_stock = Column(Numeric(10, 2), default=0, comment="安全库存")
    
    # 生产信息
    lead_time = Column(Integer, default=0, comment="生产周期(天)")
    batch_size = Column(Numeric(10, 2), default=1, comment="批量大小")
    
    # 产品类型
    product_type = Column(String(20), default="成品", comment="产品类型(原料/半成品/成品)")
    
    # 状态字段
    is_active = Column(Boolean, default=True, comment="是否激活")
    is_sellable = Column(Boolean, default=True, comment="是否可销售")
    is_purchasable = Column(Boolean, default=False, comment="是否可采购")
    is_manufacturable = Column(Boolean, default=False, comment="是否可生产")
    
    # 时间字段
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # 备注
    description = Column(Text, comment="产品描述")
    notes = Column(Text, comment="备注")
    
    # 关系
    category = relationship("ProductCategory", backref="products")
    
    def __repr__(self):
        return f"<Product(id={self.id}, code='{self.code}', name='{self.name}')>"

class BOM(Base):
    """物料清单模型"""
    __tablename__ = "boms"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, comment="产品ID")
    version = Column(String(20), default="1.0", comment="版本号")
    
    # 状态字段
    is_active = Column(Boolean, default=True, comment="是否激活")
    
    # 时间字段
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")
    effective_date = Column(DateTime(timezone=True), comment="生效日期")
    
    # 备注
    notes = Column(Text, comment="备注")
    
    # 关系
    product = relationship("Product", backref="boms")
    
    def __repr__(self):
        return f"<BOM(id={self.id}, product_id={self.product_id}, version='{self.version}')>"

class BOMLine(Base):
    """物料清单明细模型"""
    __tablename__ = "bom_lines"
    
    id = Column(Integer, primary_key=True, index=True)
    bom_id = Column(Integer, ForeignKey("boms.id"), nullable=False, comment="BOM ID")
    material_id = Column(Integer, ForeignKey("products.id"), nullable=False, comment="物料ID")
    quantity = Column(Numeric(10, 4), nullable=False, comment="用量")
    unit = Column(String(20), comment="单位")
    
    # 工艺信息
    operation_sequence = Column(Integer, comment="工序序号")
    scrap_rate = Column(Numeric(5, 2), default=0, comment="损耗率(%)")
    
    # 时间字段
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # 备注
    notes = Column(Text, comment="备注")
    
    # 关系
    bom = relationship("BOM", backref="lines")
    material = relationship("Product", foreign_keys=[material_id])
    
    def __repr__(self):
        return f"<BOMLine(id={self.id}, bom_id={self.bom_id}, material_id={self.material_id}, quantity={self.quantity})>"