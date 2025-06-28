from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Numeric, ForeignKey, Date
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class Quotation(Base):
    """报价单模型"""
    __tablename__ = "quotations"
    
    id = Column(Integer, primary_key=True, index=True)
    number = Column(String(50), unique=True, index=True, nullable=False, comment="报价单号")
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False, comment="客户ID")
    
    # 基本信息
    quote_date = Column(Date, nullable=False, comment="报价日期")
    valid_until = Column(Date, comment="有效期至")
    currency = Column(String(10), default="CNY", comment="币种")
    exchange_rate = Column(Numeric(10, 4), default=1, comment="汇率")
    
    # 金额信息
    subtotal = Column(Numeric(15, 2), default=0, comment="小计")
    tax_rate = Column(Numeric(5, 2), default=13, comment="税率(%)")
    tax_amount = Column(Numeric(15, 2), default=0, comment="税额")
    total_amount = Column(Numeric(15, 2), default=0, comment="总金额")
    
    # 状态
    status = Column(String(20), default="草稿", comment="状态(草稿/已发送/已确认/已失效)")
    
    # 时间字段
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # 备注
    notes = Column(Text, comment="备注")
    
    # 关系
    customer = relationship("Customer", backref="quotations")
    
    def __repr__(self):
        return f"<Quotation(id={self.id}, number='{self.number}', customer_id={self.customer_id})>"

class QuotationLine(Base):
    """报价单明细模型"""
    __tablename__ = "quotation_lines"
    
    id = Column(Integer, primary_key=True, index=True)
    quotation_id = Column(Integer, ForeignKey("quotations.id"), nullable=False, comment="报价单ID")
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, comment="产品ID")
    
    # 数量和价格
    quantity = Column(Numeric(10, 2), nullable=False, comment="数量")
    unit_price = Column(Numeric(15, 2), nullable=False, comment="单价")
    discount_rate = Column(Numeric(5, 2), default=0, comment="折扣率(%)")
    line_total = Column(Numeric(15, 2), nullable=False, comment="行总额")
    
    # 交期
    delivery_date = Column(Date, comment="交货日期")
    
    # 时间字段
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # 备注
    notes = Column(Text, comment="备注")
    
    # 关系
    quotation = relationship("Quotation", backref="lines")
    product = relationship("Product")
    
    def __repr__(self):
        return f"<QuotationLine(id={self.id}, quotation_id={self.quotation_id}, product_id={self.product_id})>"

class SalesOrder(Base):
    """销售订单模型"""
    __tablename__ = "sales_orders"
    
    id = Column(Integer, primary_key=True, index=True)
    number = Column(String(50), unique=True, index=True, nullable=False, comment="订单号")
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False, comment="客户ID")
    quotation_id = Column(Integer, ForeignKey("quotations.id"), comment="关联报价单ID")
    
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
    status = Column(String(20), default="待确认", comment="状态(待确认/已确认/生产中/已发货/已完成/已取消)")
    
    # 时间字段
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # 备注
    notes = Column(Text, comment="备注")
    
    # 关系
    customer = relationship("Customer", backref="sales_orders")
    quotation = relationship("Quotation")
    
    def __repr__(self):
        return f"<SalesOrder(id={self.id}, number='{self.number}', customer_id={self.customer_id})>"

class SalesOrderLine(Base):
    """销售订单明细模型"""
    __tablename__ = "sales_order_lines"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("sales_orders.id"), nullable=False, comment="订单ID")
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, comment="产品ID")
    
    # 数量和价格
    quantity = Column(Numeric(10, 2), nullable=False, comment="订单数量")
    delivered_quantity = Column(Numeric(10, 2), default=0, comment="已发货数量")
    unit_price = Column(Numeric(15, 2), nullable=False, comment="单价")
    discount_rate = Column(Numeric(5, 2), default=0, comment="折扣率(%)")
    line_total = Column(Numeric(15, 2), nullable=False, comment="行总额")
    
    # 交期
    delivery_date = Column(Date, comment="交货日期")
    
    # 状态
    status = Column(String(20), default="待生产", comment="状态(待生产/生产中/已完成)")
    
    # 时间字段
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # 备注
    notes = Column(Text, comment="备注")
    
    # 关系
    order = relationship("SalesOrder", backref="lines")
    product = relationship("Product")
    
    def __repr__(self):
        return f"<SalesOrderLine(id={self.id}, order_id={self.order_id}, product_id={self.product_id})>"

class Delivery(Base):
    """发货单模型"""
    __tablename__ = "deliveries"
    
    id = Column(Integer, primary_key=True, index=True)
    number = Column(String(50), unique=True, index=True, nullable=False, comment="发货单号")
    order_id = Column(Integer, ForeignKey("sales_orders.id"), nullable=False, comment="销售订单ID")
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False, comment="客户ID")
    
    # 基本信息
    delivery_date = Column(Date, nullable=False, comment="发货日期")
    tracking_number = Column(String(100), comment="物流单号")
    carrier = Column(String(100), comment="承运商")
    
    # 收货地址
    delivery_address = Column(String(200), comment="收货地址")
    contact_person = Column(String(50), comment="收货联系人")
    contact_phone = Column(String(20), comment="联系电话")
    
    # 状态
    status = Column(String(20), default="待发货", comment="状态(待发货/已发货/运输中/已签收)")
    
    # 时间字段
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # 备注
    notes = Column(Text, comment="备注")
    
    # 关系
    order = relationship("SalesOrder", backref="deliveries")
    customer = relationship("Customer")
    
    def __repr__(self):
        return f"<Delivery(id={self.id}, number='{self.number}', order_id={self.order_id})>"