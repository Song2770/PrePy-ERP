from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Numeric, ForeignKey, Date
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class Invoice(Base):
    """发票模型"""
    __tablename__ = "invoices"
    
    id = Column(Integer, primary_key=True, index=True)
    number = Column(String(50), unique=True, index=True, nullable=False, comment="发票号")
    invoice_type = Column(String(20), nullable=False, comment="发票类型(销售发票/采购发票)")
    
    # 关联信息
    customer_id = Column(Integer, ForeignKey("customers.id"), comment="客户ID")
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), comment="供应商ID")
    sales_order_id = Column(Integer, ForeignKey("sales_orders.id"), comment="销售订单ID")
    purchase_order_id = Column(Integer, ForeignKey("purchase_orders.id"), comment="采购订单ID")
    
    # 基本信息
    invoice_date = Column(Date, nullable=False, comment="发票日期")
    due_date = Column(Date, comment="到期日期")
    currency = Column(String(10), default="CNY", comment="币种")
    exchange_rate = Column(Numeric(10, 4), default=1, comment="汇率")
    
    # 金额信息
    subtotal = Column(Numeric(15, 2), default=0, comment="小计")
    tax_rate = Column(Numeric(5, 2), default=13, comment="税率(%)")
    tax_amount = Column(Numeric(15, 2), default=0, comment="税额")
    total_amount = Column(Numeric(15, 2), default=0, comment="总金额")
    paid_amount = Column(Numeric(15, 2), default=0, comment="已付金额")
    outstanding_amount = Column(Numeric(15, 2), default=0, comment="未付金额")
    
    # 状态
    status = Column(String(20), default="未付", comment="状态(未付/部分付款/已付/已取消)")
    
    # 时间字段
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # 备注
    notes = Column(Text, comment="备注")
    
    # 关系
    customer = relationship("Customer")
    supplier = relationship("Supplier")
    sales_order = relationship("SalesOrder")
    purchase_order = relationship("PurchaseOrder")
    
    def __repr__(self):
        return f"<Invoice(id={self.id}, number='{self.number}', invoice_type='{self.invoice_type}')>"

class InvoiceLine(Base):
    """发票明细模型"""
    __tablename__ = "invoice_lines"
    
    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id"), nullable=False, comment="发票ID")
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, comment="产品ID")
    
    # 数量和价格
    quantity = Column(Numeric(10, 2), nullable=False, comment="数量")
    unit_price = Column(Numeric(15, 2), nullable=False, comment="单价")
    discount_rate = Column(Numeric(5, 2), default=0, comment="折扣率(%)")
    line_total = Column(Numeric(15, 2), nullable=False, comment="行总额")
    
    # 时间字段
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # 备注
    notes = Column(Text, comment="备注")
    
    # 关系
    invoice = relationship("Invoice", backref="lines")
    product = relationship("Product")
    
    def __repr__(self):
        return f"<InvoiceLine(id={self.id}, invoice_id={self.invoice_id}, product_id={self.product_id})>"

class Payment(Base):
    """付款记录模型"""
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, index=True)
    number = Column(String(50), unique=True, index=True, nullable=False, comment="付款单号")
    payment_type = Column(String(20), nullable=False, comment="付款类型(收款/付款)")
    
    # 关联信息
    customer_id = Column(Integer, ForeignKey("customers.id"), comment="客户ID")
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), comment="供应商ID")
    invoice_id = Column(Integer, ForeignKey("invoices.id"), comment="发票ID")
    
    # 基本信息
    payment_date = Column(Date, nullable=False, comment="付款日期")
    amount = Column(Numeric(15, 2), nullable=False, comment="付款金额")
    currency = Column(String(10), default="CNY", comment="币种")
    exchange_rate = Column(Numeric(10, 4), default=1, comment="汇率")
    
    # 付款方式
    payment_method = Column(String(20), default="银行转账", comment="付款方式(现金/银行转账/支票/其他)")
    bank_account = Column(String(100), comment="银行账户")
    reference_number = Column(String(100), comment="参考号")
    
    # 状态
    status = Column(String(20), default="已付", comment="状态(已付/已取消)")
    
    # 时间字段
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # 备注
    notes = Column(Text, comment="备注")
    
    # 关系
    customer = relationship("Customer")
    supplier = relationship("Supplier")
    invoice = relationship("Invoice", backref="payments")
    
    def __repr__(self):
        return f"<Payment(id={self.id}, number='{self.number}', payment_type='{self.payment_type}', amount={self.amount})>"

class AccountReceivable(Base):
    """应收账款模型"""
    __tablename__ = "account_receivables"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False, comment="客户ID")
    invoice_id = Column(Integer, ForeignKey("invoices.id"), nullable=False, comment="发票ID")
    
    # 金额信息
    original_amount = Column(Numeric(15, 2), nullable=False, comment="原始金额")
    outstanding_amount = Column(Numeric(15, 2), nullable=False, comment="未收金额")
    
    # 时间信息
    invoice_date = Column(Date, nullable=False, comment="发票日期")
    due_date = Column(Date, comment="到期日期")
    
    # 账龄分析
    aging_days = Column(Integer, default=0, comment="账龄天数")
    aging_category = Column(String(20), comment="账龄分类(未到期/1-30天/31-60天/61-90天/90天以上)")
    
    # 状态
    status = Column(String(20), default="未收", comment="状态(未收/部分收款/已收/已核销)")
    
    # 时间字段
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # 关系
    customer = relationship("Customer")
    invoice = relationship("Invoice")
    
    def __repr__(self):
        return f"<AccountReceivable(id={self.id}, customer_id={self.customer_id}, outstanding_amount={self.outstanding_amount})>"

class AccountPayable(Base):
    """应付账款模型"""
    __tablename__ = "account_payables"
    
    id = Column(Integer, primary_key=True, index=True)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=False, comment="供应商ID")
    invoice_id = Column(Integer, ForeignKey("invoices.id"), nullable=False, comment="发票ID")
    
    # 金额信息
    original_amount = Column(Numeric(15, 2), nullable=False, comment="原始金额")
    outstanding_amount = Column(Numeric(15, 2), nullable=False, comment="未付金额")
    
    # 时间信息
    invoice_date = Column(Date, nullable=False, comment="发票日期")
    due_date = Column(Date, comment="到期日期")
    
    # 账龄分析
    aging_days = Column(Integer, default=0, comment="账龄天数")
    aging_category = Column(String(20), comment="账龄分类(未到期/1-30天/31-60天/61-90天/90天以上)")
    
    # 状态
    status = Column(String(20), default="未付", comment="状态(未付/部分付款/已付/已核销)")
    
    # 时间字段
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # 关系
    supplier = relationship("Supplier")
    invoice = relationship("Invoice")
    
    def __repr__(self):
        return f"<AccountPayable(id={self.id}, supplier_id={self.supplier_id}, outstanding_amount={self.outstanding_amount})>"

class Expense(Base):
    """费用模型"""
    __tablename__ = "expenses"
    
    id = Column(Integer, primary_key=True, index=True)
    number = Column(String(50), unique=True, index=True, nullable=False, comment="费用单号")
    
    # 基本信息
    expense_date = Column(Date, nullable=False, comment="费用日期")
    expense_type = Column(String(50), nullable=False, comment="费用类型")
    department = Column(String(50), comment="部门")
    employee_id = Column(Integer, ForeignKey("users.id"), comment="申请人ID")
    
    # 金额信息
    amount = Column(Numeric(15, 2), nullable=False, comment="费用金额")
    currency = Column(String(10), default="CNY", comment="币种")
    
    # 状态
    status = Column(String(20), default="待审批", comment="状态(待审批/已审批/已付款/已拒绝)")
    
    # 时间字段
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # 备注
    description = Column(Text, comment="费用描述")
    notes = Column(Text, comment="备注")
    
    # 关系
    employee = relationship("User")
    
    def __repr__(self):
        return f"<Expense(id={self.id}, number='{self.number}', expense_type='{self.expense_type}', amount={self.amount})>"