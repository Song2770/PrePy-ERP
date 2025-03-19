from fastapi import APIRouter, Depends, HTTPException, status, Query, Path, Body
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime, date
from typing import Any, Dict, List, Optional
import uuid

from ...models.user import User, UserRole
from ...models.sales import (
    Customer, CustomerContact, SalesQuotation, SalesQuotationItem, 
    SalesOrder, SalesOrderItem, SalesInvoice, SalesInvoiceItem,
    SalesDelivery, SalesDeliveryItem, QuotationStatus, OrderStatus,
    InvoiceStatus, DeliveryStatus
)
from ...config.database import get_db
from .auth import get_current_active_user
from pydantic import BaseModel, EmailStr, Field, validator

# Create router
router = APIRouter(prefix="/sales", tags=["Sales"])

# --------------------------
# Pydantic models for requests and responses
# --------------------------

# Customer Models
class CustomerBase(BaseModel):
    name: str
    code: str
    contact_person: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    tax_id: Optional[str] = None
    industry: Optional[str] = None
    customer_type: Optional[str] = None
    credit_limit: Optional[float] = None
    payment_terms: Optional[str] = None
    notes: Optional[str] = None
    is_active: bool = True

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(CustomerBase):
    name: Optional[str] = None
    code: Optional[str] = None

class CustomerResponse(CustomerBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True

# Customer Contact Models
class CustomerContactBase(BaseModel):
    name: str
    position: Optional[str] = None
    phone: Optional[str] = None
    mobile: Optional[str] = None
    email: Optional[EmailStr] = None
    is_primary: bool = False
    notes: Optional[str] = None

class CustomerContactCreate(CustomerContactBase):
    customer_id: int

class CustomerContactUpdate(CustomerContactBase):
    name: Optional[str] = None
    customer_id: Optional[int] = None

class CustomerContactResponse(CustomerContactBase):
    id: int
    customer_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True

# Quotation Item Models
class QuotationItemBase(BaseModel):
    product_id: Optional[int] = None
    description: str
    quantity: float
    unit: Optional[str] = None
    unit_price: float
    tax_rate: float = 0.0
    discount_percent: float = 0.0
    total_price: float
    notes: Optional[str] = None

class QuotationItemCreate(QuotationItemBase):
    pass

class QuotationItemUpdate(QuotationItemBase):
    description: Optional[str] = None
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    total_price: Optional[float] = None

class QuotationItemResponse(QuotationItemBase):
    id: int
    quotation_id: int
    
    class Config:
        orm_mode = True

# Quotation Models
class QuotationBase(BaseModel):
    customer_id: int
    contact_id: Optional[int] = None
    subject: str
    quotation_date: date
    valid_until: Optional[date] = None
    total_amount: float = 0.0
    tax_amount: float = 0.0
    discount_amount: float = 0.0
    grand_total: float = 0.0
    currency: str = "CNY"
    payment_terms: Optional[str] = None
    delivery_terms: Optional[str] = None
    notes: Optional[str] = None
    terms_and_conditions: Optional[str] = None

class QuotationCreate(QuotationBase):
    items: List[QuotationItemCreate]

class QuotationUpdate(BaseModel):
    customer_id: Optional[int] = None
    contact_id: Optional[int] = None
    subject: Optional[str] = None
    quotation_date: Optional[date] = None
    valid_until: Optional[date] = None
    status: Optional[str] = None
    payment_terms: Optional[str] = None
    delivery_terms: Optional[str] = None
    notes: Optional[str] = None
    terms_and_conditions: Optional[str] = None

class QuotationResponse(QuotationBase):
    id: int
    quotation_number: str
    status: str
    created_by_id: int
    created_at: datetime
    updated_at: datetime
    items: List[QuotationItemResponse] = []
    
    class Config:
        orm_mode = True

# Sales Order Item Models
class OrderItemBase(BaseModel):
    product_id: Optional[int] = None
    description: str
    quantity: float
    unit: Optional[str] = None
    unit_price: float
    tax_rate: float = 0.0
    discount_percent: float = 0.0
    total_price: float
    expected_delivery_date: Optional[date] = None
    notes: Optional[str] = None

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemUpdate(OrderItemBase):
    description: Optional[str] = None
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    total_price: Optional[float] = None
    expected_delivery_date: Optional[date] = None

class OrderItemResponse(OrderItemBase):
    id: int
    order_id: int
    delivered_quantity: float = 0.0
    pending_quantity: float
    
    class Config:
        orm_mode = True

# Order Models
class OrderBase(BaseModel):
    customer_id: int
    contact_id: Optional[int] = None
    quotation_id: Optional[int] = None
    order_date: date
    expected_delivery_date: Optional[date] = None
    total_amount: float = 0.0
    tax_amount: float = 0.0
    discount_amount: float = 0.0
    shipping_amount: float = 0.0
    grand_total: float = 0.0
    currency: str = "CNY"
    payment_terms: Optional[str] = None
    delivery_terms: Optional[str] = None
    shipping_address: Optional[str] = None
    billing_address: Optional[str] = None
    notes: Optional[str] = None
    terms_and_conditions: Optional[str] = None

class OrderCreate(OrderBase):
    items: List[OrderItemCreate]

class OrderUpdate(BaseModel):
    customer_id: Optional[int] = None
    contact_id: Optional[int] = None
    order_date: Optional[date] = None
    expected_delivery_date: Optional[date] = None
    status: Optional[str] = None
    payment_terms: Optional[str] = None
    delivery_terms: Optional[str] = None
    shipping_address: Optional[str] = None
    billing_address: Optional[str] = None
    notes: Optional[str] = None
    terms_and_conditions: Optional[str] = None

class OrderResponse(OrderBase):
    id: int
    order_number: str
    status: str
    created_by_id: int
    created_at: datetime
    updated_at: datetime
    items: List[OrderItemResponse] = []
    
    class Config:
        orm_mode = True

# Order Status Update
class OrderStatusUpdate(BaseModel):
    status: str

# --------------------------
# Customer Endpoints
# --------------------------

@router.post("/customers", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
async def create_customer(
    customer_data: CustomerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Create a new customer.
    """
    # Check if customer code already exists
    if db.query(Customer).filter(Customer.code == customer_data.code).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Customer with this code already exists"
        )
    
    # Create new customer
    customer = Customer(**customer_data.dict())
    db.add(customer)
    db.commit()
    db.refresh(customer)
    
    return customer

@router.get("/customers", response_model=List[CustomerResponse])
async def get_customers(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Get all customers.
    """
    query = db.query(Customer)
    
    # Apply search filter if provided
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (Customer.name.ilike(search_term)) |
            (Customer.code.ilike(search_term)) |
            (Customer.contact_person.ilike(search_term))
        )
    
    customers = query.offset(skip).limit(limit).all()
    return customers

@router.get("/customers/{customer_id}", response_model=CustomerResponse)
async def get_customer(
    customer_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Get a customer by ID.
    """
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    
    return customer

@router.put("/customers/{customer_id}", response_model=CustomerResponse)
async def update_customer(
    customer_data: CustomerUpdate,
    customer_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Update a customer.
    """
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    
    # Check if code is being updated and already exists
    if customer_data.code and customer_data.code != customer.code:
        if db.query(Customer).filter(Customer.code == customer_data.code).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Customer with this code already exists"
            )
    
    # Update customer fields
    for key, value in customer_data.dict(exclude_unset=True).items():
        setattr(customer, key, value)
    
    db.commit()
    db.refresh(customer)
    
    return customer

@router.delete("/customers/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> None:
    """
    Delete customer by ID.
    """
    # 仅管理员可以删除客户
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )
    
    # 删除客户及其关联的联系人
    db.query(CustomerContact).filter(CustomerContact.customer_id == customer_id).delete()
    db.delete(customer)
    db.commit()
    
    return None

# --------------------------
# Quotation Endpoints
# --------------------------

@router.post("/quotations", response_model=QuotationResponse, status_code=status.HTTP_201_CREATED)
async def create_quotation(
    quotation_data: QuotationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Create a new quotation.
    """
    # Check if customer exists
    customer = db.query(Customer).filter(Customer.id == quotation_data.customer_id).first()
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    
    # Generate quotation number
    current_year = datetime.now().year
    quotation_count = db.query(func.count(SalesQuotation.id)).scalar() or 0
    quotation_number = f"QT-{current_year}-{quotation_count + 1:04d}"
    
    # Create quotation
    quotation_dict = quotation_data.dict(exclude={"items"})
    quotation = SalesQuotation(
        **quotation_dict,
        quotation_number=quotation_number,
        status=QuotationStatus.DRAFT,
        created_by_id=current_user.id
    )
    db.add(quotation)
    db.commit()
    db.refresh(quotation)
    
    # Create quotation items
    for item_data in quotation_data.items:
        item = SalesQuotationItem(
            **item_data.dict(),
            quotation_id=quotation.id
        )
        db.add(item)
    
    db.commit()
    db.refresh(quotation)
    
    return quotation

@router.get("/quotations", response_model=List[QuotationResponse])
async def get_quotations(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    customer_id: Optional[int] = None,
    from_date: Optional[date] = None,
    to_date: Optional[date] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Get all quotations with optional filters.
    """
    query = db.query(SalesQuotation)
    
    # Apply filters
    if status:
        query = query.filter(SalesQuotation.status == status)
    
    if customer_id:
        query = query.filter(SalesQuotation.customer_id == customer_id)
    
    if from_date:
        query = query.filter(SalesQuotation.quotation_date >= from_date)
    
    if to_date:
        query = query.filter(SalesQuotation.quotation_date <= to_date)
    
    # Get result with pagination
    quotations = query.order_by(desc(SalesQuotation.quotation_date)).offset(skip).limit(limit).all()
    
    return quotations

@router.get("/quotations/{quotation_id}", response_model=QuotationResponse)
async def get_quotation(
    quotation_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Get a quotation by ID.
    """
    quotation = db.query(SalesQuotation).filter(SalesQuotation.id == quotation_id).first()
    if not quotation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quotation not found"
        )
    
    return quotation

@router.put("/quotations/{quotation_id}", response_model=QuotationResponse)
async def update_quotation(
    quotation_data: QuotationUpdate,
    quotation_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Update a quotation.
    """
    quotation = db.query(SalesQuotation).filter(SalesQuotation.id == quotation_id).first()
    if not quotation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quotation not found"
        )
    
    # Check if status can be updated
    if quotation_data.status and quotation_data.status != quotation.status:
        if quotation.status == QuotationStatus.CONVERTED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot update status of a converted quotation"
            )
        
        # Set status
        quotation.status = quotation_data.status
    
    # Update other fields
    update_data = quotation_data.dict(exclude={"status"}, exclude_unset=True)
    for key, value in update_data.items():
        setattr(quotation, key, value)
    
    db.commit()
    db.refresh(quotation)
    
    return quotation

@router.delete("/quotations/{quotation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_quotation(
    quotation_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> None:
    """
    Delete a quotation.
    """
    quotation = db.query(SalesQuotation).filter(SalesQuotation.id == quotation_id).first()
    if not quotation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quotation not found"
        )
    
    # Check if quotation can be deleted
    if quotation.status == QuotationStatus.CONVERTED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete a converted quotation"
        )
    
    # Delete quotation items first (cascade delete should handle this, but just to be safe)
    db.query(SalesQuotationItem).filter(SalesQuotationItem.quotation_id == quotation_id).delete()
    
    # Delete quotation
    db.delete(quotation)
    db.commit()

# --------------------------
# Sales Order Endpoints
# --------------------------

@router.post("/orders", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Create a new sales order.
    """
    # Check if customer exists
    customer = db.query(Customer).filter(Customer.id == order_data.customer_id).first()
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    
    # Check if quotation exists if provided
    if order_data.quotation_id:
        quotation = db.query(SalesQuotation).filter(SalesQuotation.id == order_data.quotation_id).first()
        if not quotation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Quotation not found"
            )
    
    # Generate order number (e.g., SO-YYYYMMDD-XXX)
    today = datetime.now().strftime("%Y%m%d")
    last_order = db.query(SalesOrder).filter(
        SalesOrder.order_number.like(f"SO-{today}-%")
    ).order_by(desc(SalesOrder.order_number)).first()
    
    if last_order:
        last_num = int(last_order.order_number.split("-")[-1])
        order_num = f"SO-{today}-{last_num + 1:03d}"
    else:
        order_num = f"SO-{today}-001"
    
    # Create order
    order_dict = order_data.dict(exclude={"items"})
    order = SalesOrder(
        **order_dict,
        order_number=order_num,
        status=OrderStatus.DRAFT,
        created_by_id=current_user.id
    )
    db.add(order)
    db.flush()  # Get order ID without committing
    
    # Add order items
    for item_data in order_data.items:
        item_dict = item_data.dict()
        item = SalesOrderItem(
            **item_dict,
            order_id=order.id,
            pending_quantity=item_data.quantity
        )
        db.add(item)
    
    db.commit()
    db.refresh(order)
    
    return order

@router.get("/orders", response_model=List[OrderResponse])
async def get_orders(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    customer_id: Optional[int] = None,
    from_date: Optional[date] = None,
    to_date: Optional[date] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Get all sales orders with optional filtering.
    """
    query = db.query(SalesOrder)
    
    # Apply filters
    if status:
        query = query.filter(SalesOrder.status == status)
    
    if customer_id:
        query = query.filter(SalesOrder.customer_id == customer_id)
    
    if from_date:
        query = query.filter(SalesOrder.order_date >= from_date)
    
    if to_date:
        query = query.filter(SalesOrder.order_date <= to_date)
    
    # Order by creation date, descending
    query = query.order_by(desc(SalesOrder.created_at))
    
    # Apply pagination
    orders = query.offset(skip).limit(limit).all()
    
    return orders

@router.get("/orders/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Get a sales order by ID.
    """
    order = db.query(SalesOrder).filter(SalesOrder.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    return order

@router.put("/orders/{order_id}", response_model=OrderResponse)
async def update_order(
    order_data: OrderUpdate,
    order_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Update a sales order.
    """
    order = db.query(SalesOrder).filter(SalesOrder.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    # Prevent updating completed or cancelled orders
    if order.status in [OrderStatus.COMPLETED, OrderStatus.CANCELLED]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot update order with status '{order.status}'"
        )
    
    # Update order fields
    update_data = order_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        if field == "status" and value is not None:
            try:
                setattr(order, field, OrderStatus(value))
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid status value: {value}"
                )
        elif value is not None:
            setattr(order, field, value)
    
    db.commit()
    db.refresh(order)
    
    return order

@router.put("/orders/{order_id}/status", response_model=OrderResponse)
async def update_order_status(
    status_data: OrderStatusUpdate,
    order_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Update the status of a sales order.
    """
    order = db.query(SalesOrder).filter(SalesOrder.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    try:
        order.status = OrderStatus(status_data.status)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status value: {status_data.status}"
        )
    
    db.commit()
    db.refresh(order)
    
    return order

@router.delete("/orders/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(
    order_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> None:
    """
    Delete a sales order.
    """
    order = db.query(SalesOrder).filter(SalesOrder.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    # Only allow deletion of draft orders
    if order.status != OrderStatus.DRAFT:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only draft orders can be deleted"
        )
    
    # Check if order has related deliveries or invoices
    if db.query(SalesDelivery).filter(SalesDelivery.order_id == order_id).count() > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete order with related deliveries"
        )
    
    if db.query(SalesInvoice).filter(SalesInvoice.order_id == order_id).count() > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete order with related invoices"
        )
    
    # Delete the order items first
    db.query(SalesOrderItem).filter(SalesOrderItem.order_id == order_id).delete()
    
    # Then delete the order
    db.delete(order)
    db.commit()

@router.post("/quotations/{quotation_id}/convert", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def convert_quotation_to_order(
    quotation_id: int = Path(..., gt=0),
    additional_data: dict = Body({}),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Convert a quotation to a sales order.
    """
    # Check if quotation exists
    quotation = db.query(SalesQuotation).filter(SalesQuotation.id == quotation_id).first()
    if not quotation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quotation not found"
        )
    
    # Check if quotation status allows conversion
    if quotation.status not in [QuotationStatus.APPROVED, QuotationStatus.SENT]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot convert quotation with status '{quotation.status}'"
        )
    
    # Generate order number
    today = datetime.now().strftime("%Y%m%d")
    last_order = db.query(SalesOrder).filter(
        SalesOrder.order_number.like(f"SO-{today}-%")
    ).order_by(desc(SalesOrder.order_number)).first()
    
    if last_order:
        last_num = int(last_order.order_number.split("-")[-1])
        order_num = f"SO-{today}-{last_num + 1:03d}"
    else:
        order_num = f"SO-{today}-001"
    
    # Create order from quotation
    order = SalesOrder(
        order_number=order_num,
        customer_id=quotation.customer_id,
        contact_id=quotation.contact_id,
        quotation_id=quotation.id,
        status=OrderStatus.DRAFT,
        order_date=date.today(),
        expected_delivery_date=additional_data.get("expected_delivery_date"),
        total_amount=quotation.total_amount,
        tax_amount=quotation.tax_amount,
        discount_amount=quotation.discount_amount,
        grand_total=quotation.grand_total,
        currency=quotation.currency,
        payment_terms=quotation.payment_terms,
        delivery_terms=quotation.delivery_terms,
        shipping_address=additional_data.get("shipping_address"),
        billing_address=additional_data.get("billing_address"),
        notes=quotation.notes,
        terms_and_conditions=quotation.terms_and_conditions,
        created_by_id=current_user.id
    )
    db.add(order)
    db.flush()  # Get order ID without committing
    
    # Add order items from quotation items
    quotation_items = db.query(SalesQuotationItem).filter(
        SalesQuotationItem.quotation_id == quotation_id
    ).all()
    
    for q_item in quotation_items:
        order_item = SalesOrderItem(
            order_id=order.id,
            product_id=q_item.product_id,
            quotation_item_id=q_item.id,
            description=q_item.description,
            quantity=q_item.quantity,
            unit=q_item.unit,
            unit_price=q_item.unit_price,
            tax_rate=q_item.tax_rate,
            discount_percent=q_item.discount_percent,
            total_price=q_item.total_price,
            delivered_quantity=0,
            pending_quantity=q_item.quantity,
            expected_delivery_date=additional_data.get("expected_delivery_date"),
            notes=q_item.notes
        )
        db.add(order_item)
    
    # Update quotation status to converted
    quotation.status = QuotationStatus.CONVERTED
    
    db.commit()
    db.refresh(order)
    
    return order

@router.get("/orders/{order_id}/items", response_model=List[OrderItemResponse])
async def get_order_items(
    order_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Get all items for a specific sales order.
    """
    # Check if order exists
    if not db.query(SalesOrder).filter(SalesOrder.id == order_id).first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    items = db.query(SalesOrderItem).filter(SalesOrderItem.order_id == order_id).all()
    return items

@router.post("/orders/{order_id}/items", response_model=OrderItemResponse, status_code=status.HTTP_201_CREATED)
async def add_order_item(
    item_data: OrderItemCreate,
    order_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Add an item to a sales order.
    """
    # Check if order exists
    order = db.query(SalesOrder).filter(SalesOrder.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    # Prevent updating completed or cancelled orders
    if order.status in [OrderStatus.COMPLETED, OrderStatus.CANCELLED]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot add items to order with status '{order.status}'"
        )
    
    # Create new order item
    item = SalesOrderItem(
        **item_data.dict(),
        order_id=order_id,
        delivered_quantity=0,
        pending_quantity=item_data.quantity
    )
    db.add(item)
    
    # Update order totals
    order.total_amount += item.total_price
    tax_amount = item.total_price * item.tax_rate / 100
    order.tax_amount += tax_amount
    order.grand_total = order.total_amount + order.tax_amount - order.discount_amount + order.shipping_amount
    
    db.commit()
    db.refresh(item)
    
    return item

@router.put("/orders/{order_id}/items/{item_id}", response_model=OrderItemResponse)
async def update_order_item(
    item_data: OrderItemUpdate,
    order_id: int = Path(..., gt=0),
    item_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Update an item in a sales order.
    """
    # Check if order exists
    order = db.query(SalesOrder).filter(SalesOrder.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    # Check if item exists and belongs to the order
    item = db.query(SalesOrderItem).filter(
        SalesOrderItem.id == item_id,
        SalesOrderItem.order_id == order_id
    ).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found or does not belong to the order"
        )
    
    # Prevent updating completed or cancelled orders
    if order.status in [OrderStatus.COMPLETED, OrderStatus.CANCELLED]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot update items in order with status '{order.status}'"
        )
    
    # Store old values for recalculating order totals
    old_total_price = item.total_price
    old_tax_rate = item.tax_rate
    
    # Update item fields
    update_data = item_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        if value is not None:
            setattr(item, field, value)
    
    # Update pending quantity if quantity changed
    if "quantity" in update_data:
        item.pending_quantity = max(0, update_data["quantity"] - item.delivered_quantity)
    
    # Update order totals
    old_tax_amount = old_total_price * old_tax_rate / 100
    new_tax_amount = item.total_price * item.tax_rate / 100
    
    order.total_amount = order.total_amount - old_total_price + item.total_price
    order.tax_amount = order.tax_amount - old_tax_amount + new_tax_amount
    order.grand_total = order.total_amount + order.tax_amount - order.discount_amount + order.shipping_amount
    
    db.commit()
    db.refresh(item)
    
    return item

@router.delete("/orders/{order_id}/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order_item(
    order_id: int = Path(..., gt=0),
    item_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> None:
    """
    Delete an item from a sales order.
    """
    # Check if order exists
    order = db.query(SalesOrder).filter(SalesOrder.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    # Check if item exists and belongs to the order
    item = db.query(SalesOrderItem).filter(
        SalesOrderItem.id == item_id,
        SalesOrderItem.order_id == order_id
    ).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found or does not belong to the order"
        )
    
    # Prevent updating completed or cancelled orders
    if order.status in [OrderStatus.COMPLETED, OrderStatus.CANCELLED]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot delete items from order with status '{order.status}'"
        )
    
    # Check if item has been delivered
    if item.delivered_quantity > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete item that has been partially or fully delivered"
        )
    
    # Update order totals
    tax_amount = item.total_price * item.tax_rate / 100
    order.total_amount -= item.total_price
    order.tax_amount -= tax_amount
    order.grand_total = order.total_amount + order.tax_amount - order.discount_amount + order.shipping_amount
    
    # Delete the item
    db.delete(item)
    db.commit()

@router.get("/orders/{order_id}/deliveries", response_model=List[Any])
async def get_order_deliveries(
    order_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Get all deliveries for a specific sales order.
    """
    # Check if order exists
    if not db.query(SalesOrder).filter(SalesOrder.id == order_id).first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    deliveries = db.query(SalesDelivery).filter(SalesDelivery.order_id == order_id).all()
    return deliveries

@router.get("/orders/{order_id}/invoices", response_model=List[Any])
async def get_order_invoices(
    order_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Get all invoices for a specific sales order.
    """
    # Check if order exists
    if not db.query(SalesOrder).filter(SalesOrder.id == order_id).first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    invoices = db.query(SalesInvoice).filter(SalesInvoice.order_id == order_id).all()
    return invoices

@router.get("/orders/statistics")
async def get_order_statistics(
    from_date: Optional[date] = None,
    to_date: Optional[date] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Get order statistics.
    """
    query = db.query(SalesOrder)
    
    # Apply date filters if provided
    if from_date:
        query = query.filter(SalesOrder.order_date >= from_date)
    
    if to_date:
        query = query.filter(SalesOrder.order_date <= to_date)
    
    # Count orders by status
    status_counts = {}
    for status_value in OrderStatus:
        count = query.filter(SalesOrder.status == status_value).count()
        status_counts[status_value.value] = count
    
    # Calculate total values
    total_orders = query.count()
    
    # Sum of grand_total for all orders
    total_value = db.query(func.sum(SalesOrder.grand_total)).filter(
        query.whereclause
    ).scalar() or 0
    
    # Count orders for current month
    current_month = datetime.now().replace(day=1).date()
    current_month_orders = query.filter(SalesOrder.order_date >= current_month).count()
    
    # Count orders for previous month
    if current_month.month == 1:
        prev_month = current_month.replace(year=current_month.year - 1, month=12)
    else:
        prev_month = current_month.replace(month=current_month.month - 1)
    
    prev_month_orders = db.query(SalesOrder).filter(
        SalesOrder.order_date >= prev_month,
        SalesOrder.order_date < current_month
    ).count()
    
    # Calculate month-over-month change
    mom_change = 0
    if prev_month_orders > 0:
        mom_change = ((current_month_orders - prev_month_orders) / prev_month_orders) * 100
    
    return {
        "total_orders": total_orders,
        "total_value": total_value,
        "status_counts": status_counts,
        "current_month_orders": current_month_orders,
        "previous_month_orders": prev_month_orders,
        "month_over_month_change": mom_change
    }