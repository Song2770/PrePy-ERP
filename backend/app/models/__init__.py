# Import all models to ensure they are registered with SQLAlchemy
from .user import User, UserActivity
from .sales import Customer, CustomerContact, SalesQuotation, SalesQuotationItem
from .technical import Product, BOM, BOMItem 