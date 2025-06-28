from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Numeric, ForeignKey, Date
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class Supplier(Base):
    """供应商模型"""
    __tablename__ = "suppliers"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, index=True, nullable=False, comment="供应商编码")
    name = Column(String(100), nullable=False, comment="供应商名称")
    short_name = Column(String(50), comment="供应商简称")
    
    # 联系信息
    contact_person = Column(String(50), comment="联系人")
    phone = Column(String(20), comment="电话")
    email = Column(String(100), comment="邮箱")
    fax = Column(String(20), comment="传真")
    website = Column(String(200), comment="网站")
    
    # 地址信息
    address = Column(String(200), comment="地址")
    city = Column(String(50), comment="城市")
    province = Column(String(50), comment="省份")
    country = Column(String(50), default="中国", comment="国家")
    postal_code = Column(String(10), comment="邮编")
    
    # 财务信息
    tax_number = Column(String(50), comment="税号")
    bank_name = Column(String(100), comment="开户银行")
    bank_account = Column(String(50), comment="银行账号")
    payment_terms = Column(String(50), comment="付款条件")
    
    # 分类信息
    supplier_type = Column(String(20), default="普通供应商", comment="供应商类型")
    industry = Column(String(50), comment="所属行业")
    level = Column(String(20), default="C", comment="供应商等级(A/B/C)")
    
    # 状态字段
    is_active = Column(Boolean, default=True, comment="是否激活")
    
    # 时间字段
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # 备注
    notes = Column(Text, comment="备注")
    
    def __repr__(self):
        return f"<Supplier(id={self.id}, code='{self.code}', name='{self.name}')>"

class PurchaseOrder(Base):
    """采购订单模型"""
    __tablename__ = "purchase_orders"
    
    id = Column(Integer, primary_key=True, index=True)
    number = Column(String(50), unique=True, index=True, nullable=False, comment="采购订单号")
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=False, comment="供应商ID")
    
    # 基本信息
    order_date = Column(Date, nullable=False, comment="订单日期")
    delivery_date = Column(Date, comment="交货日期")
    currency = Column(String(10), default="CNY", comment="币种")
    exchange_rate = Column(Numeric(10, 4), default=1, comment="汇率")
    
    # 金额信息
    subtotal = Column(Numeric(15, 2), default=0, comment="小计")
    tax_rate = Column(Numeric(5, 2), default=13, comment="税率(%)")
    tax_amount = Column(Numeric(15, 2), default=0, comment="税额")
    total_amount = Column(Numeric(15, 2), default=0, comment="总金额")
    
    # 付款条件
    payment_terms = Column(String(100), comment="付款条件")
    
    # 状态
    status = Column(String(20), default="待确认", comment="状态(待确认/已确认/部分到货/已到货/已完成/已取消)")
    
    # 时间字段
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # 备注
    notes = Column(Text, comment="备注")
    
    # 关系
    supplier = relationship("Supplier", backref="purchase_orders")
    
    def __repr__(self):
        return f"<PurchaseOrder(id={self.id}, number='{self.number}', supplier_id={self.supplier_id})>"

class PurchaseOrderLine(Base):
    """采购订单明细模型"""
    __tablename__ = "purchase_order_lines"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("purchase_orders.id"), nullable=False, comment="采购订单ID")
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, comment="产品ID")
    
    # 数量和价格
    quantity = Column(Numeric(10, 2), nullable=False, comment="订单数量")
    received_quantity = Column(Numeric(10, 2), default=0, comment="已收货数量")
    unit_price = Column(Numeric(15, 2), nullable=False, comment="单价")
    discount_rate = Column(Numeric(5, 2), default=0, comment="折扣率(%)")
    line_total = Column(Numeric(15, 2), nullable=False, comment="行总额")
    
    # 交期
    delivery_date = Column(Date, comment="交货日期")
    
    # 状态
    status = Column(String(20), default="待收货", comment="状态(待收货/部分收货/已收货)")
    
    # 时间字段
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # 备注
    notes = Column(Text, comment="备注")
    
    # 关系
    order = relationship("PurchaseOrder", backref="lines")
    product = relationship("Product")
    
    def __repr__(self):
        return f"<PurchaseOrderLine(id={self.id}, order_id={self.order_id}, product_id={self.product_id})>"

class PurchaseReceipt(Base):
    """采购收货单模型"""
    __tablename__ = "purchase_receipts"
    
    id = Column(Integer, primary_key=True, index=True)
    number = Column(String(50), unique=True, index=True, nullable=False, comment="收货单号")
    order_id = Column(Integer, ForeignKey("purchase_orders.id"), nullable=False, comment="采购订单ID")
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=False, comment="供应商ID")
    
    # 基本信息
    receipt_date = Column(Date, nullable=False, comment="收货日期")
    delivery_note = Column(String(100), comment="送货单号")
    
    # 状态
    status = Column(String(20), default="待检验", comment="状态(待检验/检验中/已入库/已退货)")
    
    # 时间字段
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # 备注
    notes = Column(Text, comment="备注")
    
    # 关系
    order = relationship("PurchaseOrder", backref="receipts")
    supplier = relationship("Supplier")
    
    def __repr__(self):
        return f"<PurchaseReceipt(id={self.id}, number='{self.number}', order_id={self.order_id})>"

class PurchaseReceiptLine(Base):
    """采购收货单明细模型"""
    __tablename__ = "purchase_receipt_lines"
    
    id = Column(Integer, primary_key=True, index=True)
    receipt_id = Column(Integer, ForeignKey("purchase_receipts.id"), nullable=False, comment="收货单ID")
    order_line_id = Column(Integer, ForeignKey("purchase_order_lines.id"), nullable=False, comment="采购订单明细ID")
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, comment="产品ID")
    
    # 数量信息
    received_quantity = Column(Numeric(10, 2), nullable=False, comment="收货数量")
    qualified_quantity = Column(Numeric(10, 2), default=0, comment="合格数量")
    rejected_quantity = Column(Numeric(10, 2), default=0, comment="不合格数量")
    
    # 质检信息
    inspection_status = Column(String(20), default="待检验", comment="检验状态(待检验/合格/不合格/部分合格)")
    inspector_id = Column(Integer, ForeignKey("users.id"), comment="检验员ID")
    inspection_date = Column(Date, comment="检验日期")
    
    # 时间字段
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # 备注
    notes = Column(Text, comment="备注")
    
    # 关系
    receipt = relationship("PurchaseReceipt", backref="lines")
    order_line = relationship("PurchaseOrderLine")
    product = relationship("Product")
    inspector = relationship("User")
    
    def __repr__(self):
        return f"<PurchaseReceiptLine(id={self.id}, receipt_id={self.receipt_id}, product_id={self.product_id})>"