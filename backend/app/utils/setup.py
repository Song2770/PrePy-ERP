from datetime import datetime, date
import os
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from ..models.user import User, UserRole
from ..models.sales import (
    Customer, CustomerContact, SalesQuotation, SalesQuotationItem,
    SalesOrder, SalesOrderItem, QuotationStatus, OrderStatus
)
from ..models.technical import (
    Product, BOM, BOMItem, Workstation, Operation, ProductionRoute,
    RouteOperation, TechnicalDocument, ProductCategory, UnitOfMeasure,
    BOMType, RouteStatus, DocumentStatus
)
from ..utils.auth import get_password_hash

# Load environment variables
load_dotenv()

def create_admin_user(db: Session):
    """
    Create admin user if not exists.
    """
    admin_user = db.query(User).filter(User.username == "admin").first()
    if not admin_user:
        admin_user = User(
            username="admin",
            email="admin@example.com",
            full_name="System Administrator",
            hashed_password=get_password_hash("123456"),  # Change this in production
            role=UserRole.ADMIN,
            is_active=True,
            is_superuser=True,
        )
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        print("Admin user created.")
    return admin_user

def create_sample_users(db: Session):
    """
    Create sample users if not exists.
    """
    sample_users = [
        {
            "username": "manager",
            "email": "manager@example.com",
            "full_name": "General Manager",
            "role": UserRole.ADMIN,
            "is_active": True,
            "is_superuser": True,
            "password": "password",  # Change this in production
            "department": "test",
            "position": "test",
        },
        {
            "username": "sales",
            "email": "sales@example.com",
            "full_name": "Sales Manager",
            "password": "password",  # Change this in production
            "role": UserRole.SALES,
            "department": "Sales",
            "position": "Sales Manager",
        },
        {
            "username": "technical",
            "email": "technical@example.com",
            "full_name": "Technical Manager",
            "password": "password",  # Change this in production
            "role": UserRole.TECHNICAL,
            "department": "Technical",
            "position": "Technical Manager",
        },
        {
            "username": "production",
            "email": "production@example.com",
            "full_name": "Production Manager",
            "password": "password",  # Change this in production
            "role": UserRole.PRODUCTION,
            "department": "Production",
            "position": "Production Manager",
        },
    ]
    print("Sample users created")
    
    created_users = []
    for user_data in sample_users:
        user = db.query(User).filter(User.username == user_data["username"]).first()
        if not user:
            user = User(
                username=user_data["username"],
                email=user_data["email"],
                full_name=user_data["full_name"],
                hashed_password=get_password_hash(user_data["password"]),
                role=user_data["role"],
                department=user_data["department"],
                position=user_data["position"],
                is_active=True,
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            print(f"User '{user_data['username']}' created.")
        created_users.append(user)
    
    return created_users

def create_sample_customers(db: Session):
    """
    Create sample customers if not exists.
    """
    sample_customers = [
        {
            "name": "ABC Electronics",
            "code": "CUST001",
            "contact_person": "John Smith",
            "phone": "1234567890",
            "email": "john@abcelectronics.com",
            "address": "123 Main St",
            "city": "Shanghai",
            "country": "China",
            "tax_id": "TAX123456",
            "industry": "Electronics",
            "customer_type": "Corporate",
        },
        {
            "name": "XYZ Manufacturing",
            "code": "CUST002",
            "contact_person": "Jane Doe",
            "phone": "9876543210",
            "email": "jane@xyzmanufacturing.com",
            "address": "456 Broad St",
            "city": "Beijing",
            "country": "China",
            "tax_id": "TAX654321",
            "industry": "Manufacturing",
            "customer_type": "Corporate",
        },
    ]
    
    created_customers = []
    for customer_data in sample_customers:
        customer = db.query(Customer).filter(Customer.code == customer_data["code"]).first()
        if not customer:
            customer = Customer(**customer_data)
            db.add(customer)
            db.commit()
            db.refresh(customer)
            print(f"Customer '{customer_data['name']}' created.")
            
            # Add a primary contact
            contact = CustomerContact(
                customer_id=customer.id,
                name=customer_data["contact_person"],
                phone=customer_data["phone"],
                email=customer_data["email"],
                is_primary=True,
            )
            db.add(contact)
            db.commit()
            db.refresh(contact)
        
        created_customers.append(customer)
    
    return created_customers

def create_sample_products(db: Session):
    """
    Create sample products if not exists.
    """
    sample_products = [
        {
            "code": "RM001",
            "name": "Steel Sheet",
            "category": ProductCategory.RAW_MATERIAL,
            "description": "High quality steel sheet",
            "unit": UnitOfMeasure.KG,
            "standard_cost": 5.0,
            "current_cost": 5.5,
            "selling_price": 8.0,
            "minimum_price": 6.0,
            "tax_rate": 13.0,
            "is_purchasable": True,
            "is_sellable": True,
            "is_stockable": True,
            "min_stock_level": 100.0,
            "max_stock_level": 1000.0,
            "reorder_level": 200.0,
            "lead_time": 7,
        },
        {
            "code": "COMP001",
            "name": "Electric Motor",
            "category": ProductCategory.COMPONENT,
            "description": "250W electric motor",
            "unit": UnitOfMeasure.PIECE,
            "standard_cost": 50.0,
            "current_cost": 52.0,
            "selling_price": 75.0,
            "minimum_price": 60.0,
            "tax_rate": 13.0,
            "is_purchasable": True,
            "is_sellable": True,
            "is_stockable": True,
            "min_stock_level": 20.0,
            "max_stock_level": 100.0,
            "reorder_level": 30.0,
            "lead_time": 14,
        },
        {
            "code": "FP001",
            "name": "Industrial Fan",
            "category": ProductCategory.FINISHED,
            "description": "Industrial grade cooling fan",
            "unit": UnitOfMeasure.PIECE,
            "standard_cost": 200.0,
            "current_cost": 210.0,
            "selling_price": 350.0,
            "minimum_price": 250.0,
            "tax_rate": 13.0,
            "is_purchasable": False,
            "is_sellable": True,
            "is_stockable": True,
            "min_stock_level": 5.0,
            "max_stock_level": 30.0,
            "reorder_level": 10.0,
            "lead_time": 5,
        },
    ]
    
    created_products = []
    admin_user = db.query(User).filter(User.username == "admin").first()
    
    for product_data in sample_products:
        product = db.query(Product).filter(Product.code == product_data["code"]).first()
        if not product:
            product_data["created_by_id"] = admin_user.id
            product = Product(**product_data)
            db.add(product)
            db.commit()
            db.refresh(product)
            print(f"Product '{product_data['name']}' created.")
        
        created_products.append(product)
    
    return created_products

def create_sample_boms(db: Session, products):
    """
    Create sample BOMs if not exists.
    """
    # Get products by code
    product_map = {product.code: product for product in products}
    
    # Create BOM for the finished product
    fan_product = product_map.get("FP001")
    if fan_product:
        bom = db.query(BOM).filter(BOM.code == "BOM001").first()
        admin_user = db.query(User).filter(User.username == "admin").first()
        
        if not bom:
            bom = BOM(
                product_id=fan_product.id,
                name="Industrial Fan BOM",
                code="BOM001",
                version="1.0",
                type=BOMType.MANUFACTURING,
                description="Bill of Materials for Industrial Fan",
                is_default=True,
                is_active=True,
                created_by_id=admin_user.id,
                effective_from=date.today(),
            )
            db.add(bom)
            db.commit()
            db.refresh(bom)
            print(f"BOM '{bom.name}' created.")
            
            # Add BOM items
            bom_items = [
                {
                    "component_id": product_map.get("RM001").id,
                    "position": 1,
                    "quantity": 2.5,
                    "unit": UnitOfMeasure.KG,
                    "scrap_rate": 5.0,
                },
                {
                    "component_id": product_map.get("COMP001").id,
                    "position": 2,
                    "quantity": 1.0,
                    "unit": UnitOfMeasure.PIECE,
                    "scrap_rate": 1.0,
                    "is_critical": True,
                },
            ]
            
            for item_data in bom_items:
                bom_item = BOMItem(
                    bom_id=bom.id,
                    **item_data
                )
                db.add(bom_item)
            
            db.commit()
            print("BOM items created.")
        
        return bom

def create_sample_workstations(db: Session):
    """
    Create sample workstations if not exists.
    """
    sample_workstations = [
        {
            "name": "Assembly Line 1",
            "code": "WS001",
            "description": "Main assembly line",
            "capacity": 8.0,  # 8 hours per day
            "efficiency": 90.0,
            "location": "Building A, Floor 1",
        },
        {
            "name": "Quality Control",
            "code": "WS002",
            "description": "Quality control station",
            "capacity": 8.0,
            "efficiency": 95.0,
            "location": "Building A, Floor 1",
        },
        {
            "name": "Packaging",
            "code": "WS003",
            "description": "Packaging station",
            "capacity": 8.0,
            "efficiency": 85.0,
            "location": "Building A, Floor 2",
        },
    ]
    
    created_workstations = []
    for ws_data in sample_workstations:
        workstation = db.query(Workstation).filter(Workstation.code == ws_data["code"]).first()
        if not workstation:
            workstation = Workstation(**ws_data)
            db.add(workstation)
            db.commit()
            db.refresh(workstation)
            print(f"Workstation '{ws_data['name']}' created.")
        
        created_workstations.append(workstation)
    
    return created_workstations

def initialize_db(db: Session):
    """
    Initialize database with sample data.
    """
    print("Initializing database with sample data...")
    
    # Create admin user
    admin_user = create_admin_user(db)
    
    # Create sample users
    sample_users = create_sample_users(db)
    
    # Create sample customers
    sample_customers = create_sample_customers(db)
    
    # Create sample products
    sample_products = create_sample_products(db)
    
    # Create sample BOMs
    sample_bom = create_sample_boms(db, sample_products)
    
    # Create sample workstations
    sample_workstations = create_sample_workstations(db)
    
    print("Database initialization completed.")
    
    return {
        "admin_user": admin_user,
        "sample_users": sample_users,
        "sample_customers": sample_customers,
        "sample_products": sample_products,
        "sample_bom": sample_bom,
        "sample_workstations": sample_workstations,
    } 