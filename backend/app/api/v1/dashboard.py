from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
import calendar

from ...models.user import User
from ...models.sales import (
    SalesOrder, OrderStatus, SalesQuotation,
    Customer, SalesInvoice, InvoiceStatus
)
from ...models.technical import Product, ProductCategory
from ...config.database import get_db
from ..auth import get_current_active_user

# Create router
router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/")
async def get_dashboard_data(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Get dashboard data.
    """
    # Get current date and first day of current month
    today = datetime.now().date()
    first_day_of_month = datetime(today.year, today.month, 1).date()
    
    # Count sales orders in current month
    sales_orders_count = db.query(func.count(SalesOrder.id)).filter(
        SalesOrder.order_date >= first_day_of_month,
        SalesOrder.order_date <= today
    ).scalar() or 0
    
    # Calculate sales amount in current month
    sales_amount = db.query(func.sum(SalesOrder.grand_total)).filter(
        SalesOrder.order_date >= first_day_of_month,
        SalesOrder.order_date <= today,
        SalesOrder.status != OrderStatus.CANCELLED
    ).scalar() or 0
    
    # Count total products
    products_count = db.query(func.count(Product.id)).scalar() or 0
    
    # Count total customers
    customers_count = db.query(func.count(Customer.id)).scalar() or 0
    
    # Get recent activities (simulated for now, in a real app you'd have an Activity model)
    recent_activities = []
    
    return {
        "salesOrders": sales_orders_count,
        "salesAmount": float(sales_amount),
        "productsCount": products_count,
        "customersCount": customers_count,
        "recentActivities": recent_activities
    }

@router.get("/stats")
async def get_dashboard_stats(
    period: str = Query("month", enum=["day", "week", "month", "year"]),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Get dashboard statistics based on time period.
    """
    today = datetime.now().date()
    
    # Define start date based on period
    if period == "day":
        start_date = today
    elif period == "week":
        start_date = today - timedelta(days=today.weekday())
    elif period == "month":
        start_date = datetime(today.year, today.month, 1).date()
    elif period == "year":
        start_date = datetime(today.year, 1, 1).date()
    else:
        start_date = datetime(today.year, today.month, 1).date()
    
    # Count new orders
    new_orders = db.query(func.count(SalesOrder.id)).filter(
        SalesOrder.order_date >= start_date,
        SalesOrder.order_date <= today
    ).scalar() or 0
    
    # Calculate total revenue
    revenue = db.query(func.sum(SalesOrder.grand_total)).filter(
        SalesOrder.order_date >= start_date,
        SalesOrder.order_date <= today,
        SalesOrder.status != OrderStatus.CANCELLED
    ).scalar() or 0
    
    # Count new quotations
    new_quotations = db.query(func.count(SalesQuotation.id)).filter(
        SalesQuotation.quotation_date >= start_date,
        SalesQuotation.quotation_date <= today
    ).scalar() or 0
    
    # Count new customers
    new_customers = db.query(func.count(Customer.id)).filter(
        Customer.created_at >= start_date,
        Customer.created_at <= today
    ).scalar() or 0
    
    # Calculate pending payments
    pending_payments = db.query(func.sum(SalesInvoice.amount_due)).filter(
        SalesInvoice.status == InvoiceStatus.SENT,
        SalesInvoice.invoice_date >= start_date,
        SalesInvoice.invoice_date <= today
    ).scalar() or 0
    
    return {
        "newOrders": new_orders,
        "revenue": float(revenue),
        "newQuotations": new_quotations,
        "newCustomers": new_customers,
        "pendingPayments": float(pending_payments),
        "period": period
    }

@router.get("/sales-chart")
async def get_sales_chart_data(
    period: str = Query("month", enum=["day", "week", "month", "year"]),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Get sales data for charts.
    """
    today = datetime.now().date()
    
    # Set up date ranges and labels based on period
    if period == "day":
        # Last 24 hours with hourly data
        labels = [f"{hour}:00" for hour in range(24)]
        data = [0] * 24
        # For a real implementation, you would query each hour's sales
    
    elif period == "week":
        # Current week with daily data
        start_date = today - timedelta(days=today.weekday())
        labels = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        data = [0] * 7
        
        # Get daily sales for current week
        for i in range(7):
            day_date = start_date + timedelta(days=i)
            if day_date <= today:
                day_sales = db.query(func.sum(SalesOrder.grand_total)).filter(
                    SalesOrder.order_date == day_date,
                    SalesOrder.status != OrderStatus.CANCELLED
                ).scalar() or 0
                data[i] = float(day_sales)
    
    elif period == "month":
        # Current month with daily data
        start_date = datetime(today.year, today.month, 1).date()
        days_in_month = calendar.monthrange(today.year, today.month)[1]
        labels = [str(day) for day in range(1, days_in_month + 1)]
        data = [0] * days_in_month
        
        # Get daily sales for current month
        for i in range(min(today.day, days_in_month)):
            day_date = start_date + timedelta(days=i)
            day_sales = db.query(func.sum(SalesOrder.grand_total)).filter(
                SalesOrder.order_date == day_date,
                SalesOrder.status != OrderStatus.CANCELLED
            ).scalar() or 0
            data[i] = float(day_sales)
    
    else:  # year
        # Current year with monthly data
        labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        data = [0] * 12
        
        # Get monthly sales for current year
        for i in range(1, 13):
            month_start = datetime(today.year, i, 1).date()
            if i == 12:
                month_end = datetime(today.year + 1, 1, 1).date() - timedelta(days=1)
            else:
                month_end = datetime(today.year, i + 1, 1).date() - timedelta(days=1)
            
            if month_end <= today:
                month_sales = db.query(func.sum(SalesOrder.grand_total)).filter(
                    SalesOrder.order_date >= month_start,
                    SalesOrder.order_date <= month_end,
                    SalesOrder.status != OrderStatus.CANCELLED
                ).scalar() or 0
                data[i - 1] = float(month_sales)
    
    return {
        "labels": labels,
        "data": data,
        "period": period
    }

@router.get("/inventory-status")
async def get_inventory_status(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Get inventory status.
    """
    # Count products by category
    raw_materials = db.query(func.count(Product.id)).filter(
        Product.category == ProductCategory.RAW_MATERIAL
    ).scalar() or 0
    
    components = db.query(func.count(Product.id)).filter(
        Product.category == ProductCategory.COMPONENT
    ).scalar() or 0
    
    semi_finished = db.query(func.count(Product.id)).filter(
        Product.category == ProductCategory.SEMI_FINISHED
    ).scalar() or 0
    
    finished = db.query(func.count(Product.id)).filter(
        Product.category == ProductCategory.FINISHED
    ).scalar() or 0
    
    # Get low stock products (where current stock is below reorder level)
    # In a real app, you would have a Stock model
    low_stock_products = []
    
    return {
        "productsByCategory": {
            "rawMaterials": raw_materials,
            "components": components,
            "semiFinished": semi_finished,
            "finished": finished
        },
        "lowStockProducts": low_stock_products
    }

@router.get("/activities")
async def get_recent_activities(
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Get recent activities.
    """
    # In a real app, you would query the Activity model
    # For now, return simulated data
    activities = [
        {
            "date": (datetime.now() - timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S"),
            "type": "登录",
            "description": "用户登录系统",
            "user": "管理员"
        },
        {
            "date": (datetime.now() - timedelta(hours=2)).strftime("%Y-%m-%d %H:%M:%S"),
            "type": "创建",
            "description": "创建了新的销售订单 #SO-2023001",
            "user": "销售经理"
        },
        {
            "date": (datetime.now() - timedelta(hours=3)).strftime("%Y-%m-%d %H:%M:%S"),
            "type": "更新",
            "description": "更新了产品"工业风扇"的价格",
            "user": "产品经理"
        },
        {
            "date": (datetime.now() - timedelta(hours=4)).strftime("%Y-%m-%d %H:%M:%S"),
            "type": "发货",
            "description": "销售订单 #SO-2023001 已发货",
            "user": "仓库管理员"
        }
    ]
    
    return activities[:limit] 