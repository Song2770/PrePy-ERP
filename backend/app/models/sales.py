from sqlalchemy import (
    Boolean, Column, ForeignKey, Integer, String, 
    DateTime, Text, Enum, Float, Date, Table, UniqueConstraint
)
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from ..config.database import Base

# Enums for sales module
class QuotationStatus(str, enum.Enum):
    """Quotation status enum"""
    DRAFT = "draft"
    SENT = "sent"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"
    CONVERTED = "converted"  # Converted to sales order

class OrderStatus(str, enum.Enum):
    """Order status enum"""
    DRAFT = "draft"
    CONFIRMED = "confirmed"
    IN_PRODUCTION = "in_production"
    READY_FOR_SHIPMENT = "ready_for_shipment"
    PARTIALLY_SHIPPED = "partially_shipped"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class InvoiceStatus(str, enum.Enum):
    """Invoice status enum"""
    DRAFT = "draft"
    SENT = "sent"
    PARTIALLY_PAID = "partially_paid"
    PAID = "paid"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"

class DeliveryStatus(str, enum.Enum):
    """Delivery status enum"""
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    RETURNED = "returned"
    CANCELLED = "cancelled"

class PaymentMethod(str, enum.Enum):
    """Payment method enum"""
    CASH = "cash"
    BANK_TRANSFER = "bank_transfer"
    CREDIT_CARD = "credit_card"
    CHECK = "check"
    ONLINE_PAYMENT = "online_payment"

class Customer(Base):
    """Customer model"""
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    code = Column(String, unique=True, index=True)
    contact_person = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)
    address = Column(Text, nullable=True)
    city = Column(String, nullable=True)
    state = Column(String, nullable=True)
    country = Column(String, nullable=True)
    postal_code = Column(String, nullable=True)
    tax_id = Column(String, nullable=True)
    industry = Column(String, nullable=True)
    customer_type = Column(String, nullable=True)
    credit_limit = Column(Float, nullable=True)
    payment_terms = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    quotations = relationship("SalesQuotation", back_populates="customer")
    orders = relationship("SalesOrder", back_populates="customer")
    contacts = relationship("CustomerContact", back_populates="customer")

    def __repr__(self):
        return f"<Customer {self.name}>"

class CustomerContact(Base):
    """Customer contact model"""
    __tablename__ = "customer_contacts"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id", ondelete="CASCADE"))
    name = Column(String)
    position = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    mobile = Column(String, nullable=True)
    email = Column(String, nullable=True)
    is_primary = Column(Boolean, default=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    customer = relationship("Customer", back_populates="contacts")

    def __repr__(self):
        return f"<CustomerContact {self.name}>"

class SalesQuotation(Base):
    """Sales quotation model"""
    __tablename__ = "sales_quotations"

    id = Column(Integer, primary_key=True, index=True)
    quotation_number = Column(String, unique=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    contact_id = Column(Integer, ForeignKey("customer_contacts.id"), nullable=True)
    status = Column(Enum(QuotationStatus), default=QuotationStatus.DRAFT)
    subject = Column(String)
    quotation_date = Column(Date)
    valid_until = Column(Date, nullable=True)
    total_amount = Column(Float, default=0.0)
    tax_amount = Column(Float, default=0.0)
    discount_amount = Column(Float, default=0.0)
    grand_total = Column(Float, default=0.0)
    currency = Column(String, default="CNY")
    payment_terms = Column(Text, nullable=True)
    delivery_terms = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    terms_and_conditions = Column(Text, nullable=True)
    created_by_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    customer = relationship("Customer", back_populates="quotations")
    contact = relationship("CustomerContact")
    items = relationship("SalesQuotationItem", back_populates="quotation", cascade="all, delete-orphan")
    created_by = relationship("User", back_populates="sales_quotations")

    def __repr__(self):
        return f"<SalesQuotation {self.quotation_number}>"

class SalesQuotationItem(Base):
    """Sales quotation item model"""
    __tablename__ = "sales_quotation_items"

    id = Column(Integer, primary_key=True, index=True)
    quotation_id = Column(Integer, ForeignKey("sales_quotations.id", ondelete="CASCADE"))
    product_id = Column(Integer, ForeignKey("products.id"), nullable=True)
    description = Column(Text)
    quantity = Column(Float)
    unit = Column(String, nullable=True)
    unit_price = Column(Float)
    tax_rate = Column(Float, default=0.0)
    discount_percent = Column(Float, default=0.0)
    total_price = Column(Float)
    notes = Column(Text, nullable=True)

    # Relationships
    quotation = relationship("SalesQuotation", back_populates="items")
    product = relationship("Product")

    def __repr__(self):
        return f"<SalesQuotationItem {self.id}>"

class SalesOrder(Base):
    """Sales order model"""
    __tablename__ = "sales_orders"

    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String, unique=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    contact_id = Column(Integer, ForeignKey("customer_contacts.id"), nullable=True)
    quotation_id = Column(Integer, ForeignKey("sales_quotations.id"), nullable=True)
    status = Column(Enum(OrderStatus), default=OrderStatus.DRAFT)
    order_date = Column(Date)
    expected_delivery_date = Column(Date, nullable=True)
    total_amount = Column(Float, default=0.0)
    tax_amount = Column(Float, default=0.0)
    discount_amount = Column(Float, default=0.0)
    shipping_amount = Column(Float, default=0.0)
    grand_total = Column(Float, default=0.0)
    currency = Column(String, default="CNY")
    payment_terms = Column(Text, nullable=True)
    delivery_terms = Column(Text, nullable=True)
    shipping_address = Column(Text, nullable=True)
    billing_address = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    terms_and_conditions = Column(Text, nullable=True)
    created_by_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    customer = relationship("Customer", back_populates="orders")
    contact = relationship("CustomerContact")
    quotation = relationship("SalesQuotation")
    items = relationship("SalesOrderItem", back_populates="order", cascade="all, delete-orphan")
    invoices = relationship("SalesInvoice", back_populates="order")
    deliveries = relationship("SalesDelivery", back_populates="order")
    created_by = relationship("User", back_populates="sales_orders")

    def __repr__(self):
        return f"<SalesOrder {self.order_number}>"

class SalesOrderItem(Base):
    """Sales order item model"""
    __tablename__ = "sales_order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("sales_orders.id", ondelete="CASCADE"))
    product_id = Column(Integer, ForeignKey("products.id"), nullable=True)
    quotation_item_id = Column(Integer, ForeignKey("sales_quotation_items.id"), nullable=True)
    description = Column(Text)
    quantity = Column(Float)
    unit = Column(String, nullable=True)
    unit_price = Column(Float)
    tax_rate = Column(Float, default=0.0)
    discount_percent = Column(Float, default=0.0)
    total_price = Column(Float)
    delivered_quantity = Column(Float, default=0.0)
    pending_quantity = Column(Float)
    expected_delivery_date = Column(Date, nullable=True)
    notes = Column(Text, nullable=True)

    # Relationships
    order = relationship("SalesOrder", back_populates="items")
    product = relationship("Product")
    quotation_item = relationship("SalesQuotationItem")

    def __repr__(self):
        return f"<SalesOrderItem {self.id}>"

class SalesInvoice(Base):
    """Sales invoice model"""
    __tablename__ = "sales_invoices"

    id = Column(Integer, primary_key=True, index=True)
    invoice_number = Column(String, unique=True, index=True)
    order_id = Column(Integer, ForeignKey("sales_orders.id"))
    customer_id = Column(Integer, ForeignKey("customers.id"))
    status = Column(Enum(InvoiceStatus), default=InvoiceStatus.DRAFT)
    invoice_date = Column(Date)
    due_date = Column(Date)
    total_amount = Column(Float, default=0.0)
    tax_amount = Column(Float, default=0.0)
    discount_amount = Column(Float, default=0.0)
    shipping_amount = Column(Float, default=0.0)
    grand_total = Column(Float, default=0.0)
    amount_paid = Column(Float, default=0.0)
    amount_due = Column(Float, default=0.0)
    currency = Column(String, default="CNY")
    payment_terms = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    created_by_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    order = relationship("SalesOrder", back_populates="invoices")
    customer = relationship("Customer")
    items = relationship("SalesInvoiceItem", back_populates="invoice", cascade="all, delete-orphan")
    payments = relationship("SalesPayment", back_populates="invoice")

    def __repr__(self):
        return f"<SalesInvoice {self.invoice_number}>"

class SalesInvoiceItem(Base):
    """Sales invoice item model"""
    __tablename__ = "sales_invoice_items"

    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey("sales_invoices.id", ondelete="CASCADE"))
    order_item_id = Column(Integer, ForeignKey("sales_order_items.id"), nullable=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=True)
    description = Column(Text)
    quantity = Column(Float)
    unit = Column(String, nullable=True)
    unit_price = Column(Float)
    tax_rate = Column(Float, default=0.0)
    discount_percent = Column(Float, default=0.0)
    total_price = Column(Float)
    notes = Column(Text, nullable=True)

    # Relationships
    invoice = relationship("SalesInvoice", back_populates="items")
    order_item = relationship("SalesOrderItem")
    product = relationship("Product")

    def __repr__(self):
        return f"<SalesInvoiceItem {self.id}>"

class SalesPayment(Base):
    """Sales payment model"""
    __tablename__ = "sales_payments"

    id = Column(Integer, primary_key=True, index=True)
    payment_number = Column(String, unique=True, index=True)
    invoice_id = Column(Integer, ForeignKey("sales_invoices.id"))
    customer_id = Column(Integer, ForeignKey("customers.id"))
    payment_date = Column(Date)
    amount = Column(Float)
    payment_method = Column(Enum(PaymentMethod))
    reference_number = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
    created_by_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    invoice = relationship("SalesInvoice", back_populates="payments")
    customer = relationship("Customer")

    def __repr__(self):
        return f"<SalesPayment {self.payment_number}>"

class SalesDelivery(Base):
    """Sales delivery model"""
    __tablename__ = "sales_deliveries"

    id = Column(Integer, primary_key=True, index=True)
    delivery_number = Column(String, unique=True, index=True)
    order_id = Column(Integer, ForeignKey("sales_orders.id"))
    customer_id = Column(Integer, ForeignKey("customers.id"))
    status = Column(Enum(DeliveryStatus), default=DeliveryStatus.PENDING)
    delivery_date = Column(Date)
    shipping_address = Column(Text)
    tracking_number = Column(String, nullable=True)
    carrier = Column(String, nullable=True)
    packaging_notes = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    created_by_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    order = relationship("SalesOrder", back_populates="deliveries")
    customer = relationship("Customer")
    items = relationship("SalesDeliveryItem", back_populates="delivery", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<SalesDelivery {self.delivery_number}>"

class SalesDeliveryItem(Base):
    """Sales delivery item model"""
    __tablename__ = "sales_delivery_items"

    id = Column(Integer, primary_key=True, index=True)
    delivery_id = Column(Integer, ForeignKey("sales_deliveries.id", ondelete="CASCADE"))
    order_item_id = Column(Integer, ForeignKey("sales_order_items.id"))
    product_id = Column(Integer, ForeignKey("products.id"), nullable=True)
    description = Column(Text)
    quantity = Column(Float)
    notes = Column(Text, nullable=True)

    # Relationships
    delivery = relationship("SalesDelivery", back_populates="items")
    order_item = relationship("SalesOrderItem")
    product = relationship("Product")

    def __repr__(self):
        return f"<SalesDeliveryItem {self.id}>"

class SalesReturn(Base):
    """Sales return model"""
    __tablename__ = "sales_returns"

    id = Column(Integer, primary_key=True, index=True)
    return_number = Column(String, unique=True, index=True)
    order_id = Column(Integer, ForeignKey("sales_orders.id"))
    delivery_id = Column(Integer, ForeignKey("sales_deliveries.id"), nullable=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    return_date = Column(Date)
    reason = Column(Text)
    total_amount = Column(Float, default=0.0)
    notes = Column(Text, nullable=True)
    created_by_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    order = relationship("SalesOrder")
    delivery = relationship("SalesDelivery")
    customer = relationship("Customer")
    items = relationship("SalesReturnItem", back_populates="return_", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<SalesReturn {self.return_number}>"

class SalesReturnItem(Base):
    """Sales return item model"""
    __tablename__ = "sales_return_items"

    id = Column(Integer, primary_key=True, index=True)
    return_id = Column(Integer, ForeignKey("sales_returns.id", ondelete="CASCADE"))
    order_item_id = Column(Integer, ForeignKey("sales_order_items.id"))
    product_id = Column(Integer, ForeignKey("products.id"), nullable=True)
    description = Column(Text)
    quantity = Column(Float)
    unit = Column(String, nullable=True)
    unit_price = Column(Float)
    total_price = Column(Float)
    reason = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)

    # Relationships
    return_ = relationship("SalesReturn", back_populates="items")
    order_item = relationship("SalesOrderItem")
    product = relationship("Product")

    def __repr__(self):
        return f"<SalesReturnItem {self.id}>" 