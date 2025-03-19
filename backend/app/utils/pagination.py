from typing import TypeVar, Generic, List, Optional
from pydantic import BaseModel
from sqlalchemy.orm import Query
from math import ceil

T = TypeVar("T")

class PaginatedResponse(BaseModel, Generic[T]):
    """分页响应模型"""
    items: List[T]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool

    class Config:
        arbitrary_types_allowed = True

def paginate(query: Query, page: int = 1, page_size: int = 10) -> PaginatedResponse:
    """
    对查询结果进行分页
    
    Args:
        query: SQLAlchemy查询
        page: 当前页码
        page_size: 每页条数
    
    Returns:
        包含分页信息的响应对象
    """
    total = query.count()
    items = query.limit(page_size).offset((page - 1) * page_size).all()
    total_pages = ceil(total / page_size) if total > 0 else 0
    
    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        has_next=page < total_pages,
        has_prev=page > 1
    ) 