from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Text, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from ..config.database import Base

class UserRole(str, enum.Enum):
    """User role enum"""
    ADMIN = "admin"
    MANAGER = "manager"
    SALES = "sales"
    TECHNICAL = "technical"
    PLANNING = "planning"
    PRODUCTION = "production"
    PURCHASING = "purchasing"
    INVENTORY = "inventory"
    FINANCE = "finance"
    SCM = "scm"
    CRM = "crm"
    HR = "hr"
    EMPLOYEE = "employee"

class User(Base):
    """User model"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String)
    role = Column(Enum(UserRole), default=UserRole.EMPLOYEE)
    department = Column(String, nullable=True)
    position = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)

    # Define relationships to other tables
    # For example, a user can have multiple activities
    activities = relationship("UserActivity", back_populates="user")
    
    # Sales related relationships
    sales_quotations = relationship("SalesQuotation", back_populates="created_by")
    sales_orders = relationship("SalesOrder", back_populates="created_by")
    
    # HR related relationships
    # employee_info = relationship("Employee", back_populates="user", uselist=False)
    # attendance_records = relationship("Attendance", back_populates="user")
    # leave_requests = relationship("LeaveRequest", back_populates="user")
    
    def __repr__(self):
        return f"<User {self.username}>"

class UserActivity(Base):
    """User activity log model"""
    __tablename__ = "user_activities"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    activity_type = Column(String, index=True)  # login, logout, create, update, delete, etc.
    entity_type = Column(String, nullable=True)  # which entity was affected (e.g., "sales_order")
    entity_id = Column(Integer, nullable=True)   # id of the affected entity
    description = Column(Text, nullable=True)
    ip_address = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="activities") 