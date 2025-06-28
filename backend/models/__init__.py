# 导入所有模型，确保它们被SQLAlchemy识别

from .user import User, Role, UserRole
from .customer import Customer, CustomerContact
from .product import ProductCategory, Product, BOM, BOMLine
from .sales import Quotation, QuotationLine, SalesOrder, SalesOrderLine, Delivery
from .production import WorkOrder, WorkOrderOperation, Operation, WorkCenter, ProductionRecord
from .procurement import Supplier, PurchaseOrder, PurchaseOrderLine, PurchaseReceipt, PurchaseReceiptLine
from .warehouse import Warehouse, Location, Inventory, StockMovement, StockTaking, StockTakingLine
from .finance import Invoice, InvoiceLine, Payment, AccountReceivable, AccountPayable, Expense

# 导出所有模型
__all__ = [
    # 用户管理
    "User", "Role", "UserRole",
    
    # 客户管理
    "Customer", "CustomerContact",
    
    # 产品管理
    "ProductCategory", "Product", "BOM", "BOMLine",
    
    # 销售管理
    "Quotation", "QuotationLine", "SalesOrder", "SalesOrderLine", "Delivery",
    
    # 生产管理
    "WorkOrder", "WorkOrderOperation", "Operation", "WorkCenter", "ProductionRecord",
    
    # 采购管理
    "Supplier", "PurchaseOrder", "PurchaseOrderLine", "PurchaseReceipt", "PurchaseReceiptLine",
    
    # 仓库管理
    "Warehouse", "Location", "Inventory", "StockMovement", "StockTaking", "StockTakingLine",
    
    # 财务管理
    "Invoice", "InvoiceLine", "Payment", "AccountReceivable", "AccountPayable", "Expense"
]

print("模型加载完成 - 共加载 {} 个模型".format(len(__all__)))