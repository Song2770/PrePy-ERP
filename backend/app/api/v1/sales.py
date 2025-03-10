from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime, date
from typing import Any, Dict, List, Optional
import uuid

from ...models.user import User
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
    customer_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Delete a customer.
    """
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    
    # Check if customer has related records
    # In a real application, you might want to prevent deletion if there are related records
    # or implement a soft delete mechanism
    
    db.delete(customer)
    db.commit()

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

# Additional endpoints would be added for:
# - Quotation items management
# - Converting quotation to order
# - Sales orders management
# - Sales invoices
# - Sales deliveries
# - etc. 