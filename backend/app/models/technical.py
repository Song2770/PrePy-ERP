from sqlalchemy import (
    Boolean, Column, ForeignKey, Integer, String, 
    DateTime, Text, Enum, Float, Date, Table, UniqueConstraint, JSON
)
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from ..config.database import Base

# Enums for technical module
class ProductCategory(str, enum.Enum):
    """Product category enum"""
    RAW_MATERIAL = "raw_material"
    COMPONENT = "component"
    SEMI_FINISHED = "semi_finished"
    FINISHED = "finished"
    SERVICE = "service"

class UnitOfMeasure(str, enum.Enum):
    """Unit of measure enum"""
    PIECE = "piece"
    KG = "kg"
    METER = "meter"
    LITER = "liter"
    HOUR = "hour"
    SET = "set"
    PACKAGE = "package"

class BOMType(str, enum.Enum):
    """BOM type enum"""
    MANUFACTURING = "manufacturing"
    ENGINEERING = "engineering"
    SALES = "sales"
    TEMPLATE = "template"

class DocumentStatus(str, enum.Enum):
    """Document status enum"""
    DRAFT = "draft"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    OBSOLETE = "obsolete"

class RouteStatus(str, enum.Enum):
    """Production route status enum"""
    DRAFT = "draft"
    ACTIVE = "active"
    INACTIVE = "inactive"

class Product(Base):
    """Product model"""
    __tablename__ = "products"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True)
    name = Column(String, index=True)
    category = Column(Enum(ProductCategory))
    description = Column(Text, nullable=True)
    uom = Column(Enum(UnitOfMeasure), default=UnitOfMeasure.PIECE)
    standard_cost = Column(Float, default=0.0)
    current_cost = Column(Float, default=0.0)
    selling_price = Column(Float, default=0.0)
    minimum_price = Column(Float, default=0.0)
    tax_rate = Column(Float, default=0.0)
    barcode = Column(String, nullable=True)
    specifications = Column(JSON, nullable=True)
    dimensions = Column(String, nullable=True)
    weight = Column(Float, nullable=True)
    weight_unit = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_purchasable = Column(Boolean, default=True)
    is_sellable = Column(Boolean, default=True)
    is_stockable = Column(Boolean, default=True)
    min_stock_level = Column(Float, nullable=True)
    max_stock_level = Column(Float, nullable=True)
    reorder_level = Column(Float, nullable=True)
    lead_time = Column(Integer, nullable=True)  # In days
    shelf_life = Column(Integer, nullable=True)  # In days
    notes = Column(Text, nullable=True)
    created_by_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    boms = relationship("BOM", back_populates="product")
    routes = relationship("ProductionRoute", back_populates="product")
    
    def __repr__(self):
        return f"<Product {self.code} - {self.name}>"

class BOM(Base):
    """Bill of Materials model"""
    __tablename__ = "boms"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    name = Column(String)
    code = Column(String, unique=True, index=True)
    version = Column(String)
    type = Column(Enum(BOMType), default=BOMType.MANUFACTURING)
    description = Column(Text, nullable=True)
    is_default = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    reference = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
    effective_from = Column(Date, nullable=True)
    effective_to = Column(Date, nullable=True)
    approved_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    approved_at = Column(DateTime, nullable=True)
    created_by_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    product = relationship("Product", back_populates="boms")
    items = relationship("BOMItem", back_populates="bom", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<BOM {self.code} - {self.name}>"

class BOMItem(Base):
    """Bill of Materials Item model"""
    __tablename__ = "bom_items"

    id = Column(Integer, primary_key=True, index=True)
    bom_id = Column(Integer, ForeignKey("boms.id", ondelete="CASCADE"))
    component_id = Column(Integer, ForeignKey("products.id"))
    position = Column(Integer, nullable=True)
    quantity = Column(Float)
    unit = Column(Enum(UnitOfMeasure))
    scrap_rate = Column(Float, default=0.0)  # In percentage
    is_critical = Column(Boolean, default=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    bom = relationship("BOM", back_populates="items")
    component = relationship("Product")
    
    def __repr__(self):
        return f"<BOMItem {self.id}>"

class Workstation(Base):
    """Workstation model"""
    __tablename__ = "workstations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    code = Column(String, unique=True, index=True)
    description = Column(Text, nullable=True)
    capacity = Column(Float, nullable=True)  # Capacity in hours per day
    efficiency = Column(Float, default=100.0)  # In percentage
    location = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    operations = relationship("Operation", back_populates="workstation")
    
    def __repr__(self):
        return f"<Workstation {self.code} - {self.name}>"

class Operation(Base):
    """Operation model"""
    __tablename__ = "operations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    code = Column(String, unique=True, index=True)
    description = Column(Text, nullable=True)
    workstation_id = Column(Integer, ForeignKey("workstations.id"))
    setup_time = Column(Float, default=0.0)  # In minutes
    runtime = Column(Float, default=0.0)  # In minutes per unit
    teardown_time = Column(Float, default=0.0)  # In minutes
    queue_time = Column(Float, default=0.0)  # In minutes
    move_time = Column(Float, default=0.0)  # In minutes
    quality_check_required = Column(Boolean, default=False)
    special_tools = Column(Text, nullable=True)
    skill_requirements = Column(Text, nullable=True)
    instructions = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    workstation = relationship("Workstation", back_populates="operations")
    route_operations = relationship("RouteOperation", back_populates="operation")
    
    def __repr__(self):
        return f"<Operation {self.code} - {self.name}>"

class ProductionRoute(Base):
    """Production Route model"""
    __tablename__ = "production_routes"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    name = Column(String)
    code = Column(String, unique=True, index=True)
    version = Column(String)
    description = Column(Text, nullable=True)
    status = Column(Enum(RouteStatus), default=RouteStatus.DRAFT)
    is_default = Column(Boolean, default=False)
    batch_size = Column(Float, nullable=True)
    cycle_time = Column(Float, nullable=True)  # Total time in minutes
    notes = Column(Text, nullable=True)
    created_by_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    product = relationship("Product", back_populates="routes")
    operations = relationship("RouteOperation", back_populates="route", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<ProductionRoute {self.code} - {self.name}>"

class RouteOperation(Base):
    """Route Operation model"""
    __tablename__ = "route_operations"

    id = Column(Integer, primary_key=True, index=True)
    route_id = Column(Integer, ForeignKey("production_routes.id", ondelete="CASCADE"))
    operation_id = Column(Integer, ForeignKey("operations.id"))
    sequence = Column(Integer)
    description = Column(Text, nullable=True)
    setup_time = Column(Float, nullable=True)  # Override operation setup time
    runtime = Column(Float, nullable=True)  # Override operation runtime
    teardown_time = Column(Float, nullable=True)  # Override operation teardown time
    queue_time = Column(Float, nullable=True)  # Override operation queue time
    move_time = Column(Float, nullable=True)  # Override operation move time
    instructions = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    route = relationship("ProductionRoute", back_populates="operations")
    operation = relationship("Operation", back_populates="route_operations")
    
    def __repr__(self):
        return f"<RouteOperation {self.id}>"

class TechnicalDocument(Base):
    """Technical Document model"""
    __tablename__ = "technical_documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    document_number = Column(String, unique=True, index=True)
    document_type = Column(String)  # Drawing, Specification, Instruction, etc.
    version = Column(String)
    status = Column(Enum(DocumentStatus), default=DocumentStatus.DRAFT)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=True)
    bom_id = Column(Integer, ForeignKey("boms.id"), nullable=True)
    route_id = Column(Integer, ForeignKey("production_routes.id"), nullable=True)
    description = Column(Text, nullable=True)
    file_path = Column(String, nullable=True)
    file_type = Column(String, nullable=True)
    file_size = Column(Integer, nullable=True)  # In bytes
    issue_date = Column(Date, nullable=True)
    review_date = Column(Date, nullable=True)
    next_review_date = Column(Date, nullable=True)
    approved_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    approved_at = Column(DateTime, nullable=True)
    created_by_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    product = relationship("Product")
    bom = relationship("BOM")
    route = relationship("ProductionRoute")
    
    def __repr__(self):
        return f"<TechnicalDocument {self.document_number} - {self.title}>"