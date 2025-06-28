from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Numeric, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class Customer(Base):
    """客户模型"""
    __tablename__ = "customers"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, index=True, nullable=False, comment="客户编码")
    name = Column(String(100), nullable=False, comment="客户名称")
    short_name = Column(String(50), comment="客户简称")
    
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
    credit_limit = Column(Numeric(15, 2), default=0, comment="信用额度")
    payment_terms = Column(String(50), comment="付款条件")
    
    # 分类信息
    customer_type = Column(String(20), default="普通客户", comment="客户类型")
    industry = Column(String(50), comment="所属行业")
    source = Column(String(50), comment="客户来源")
    level = Column(String(20), default="C", comment="客户等级(A/B/C)")
    
    # 状态字段
    is_active = Column(Boolean, default=True, comment="是否激活")
    
    # 时间字段
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # 备注
    notes = Column(Text, comment="备注")
    
    def __repr__(self):
        return f"<Customer(id={self.id}, code='{self.code}', name='{self.name}')>"

class CustomerContact(Base):
    """客户联系人模型"""
    __tablename__ = "customer_contacts"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False, comment="客户ID")
    name = Column(String(50), nullable=False, comment="联系人姓名")
    position = Column(String(50), comment="职位")
    department = Column(String(50), comment="部门")
    phone = Column(String(20), comment="电话")
    mobile = Column(String(20), comment="手机")
    email = Column(String(100), comment="邮箱")
    
    # 状态字段
    is_primary = Column(Boolean, default=False, comment="是否主要联系人")
    is_active = Column(Boolean, default=True, comment="是否激活")
    
    # 时间字段
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # 备注
    notes = Column(Text, comment="备注")
    
    # 关系
    customer = relationship("Customer", backref="contacts")
    
    def __repr__(self):
        return f"<CustomerContact(id={self.id}, name='{self.name}', customer_id={self.customer_id})>"