from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
import uvicorn
from contextlib import asynccontextmanager

# 导入路由模块
from routers import (
    auth, users, customers, products, sales, 
    production, procurement, warehouse, finance
)
from database import init_db
from config import settings

print("正在初始化PrePy ERP系统...")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时初始化数据库
    print("正在连接数据库...")
    await init_db()
    print("数据库连接成功")
    yield
    # 关闭时清理资源
    print("正在关闭系统...")

app = FastAPI(
    title="PrePy ERP API",
    description="基于FastAPI的企业资源计划系统",
    version="1.0.0",
    lifespan=lifespan
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # Vue开发服务器
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()

# 注册路由
app.include_router(auth.router, prefix="/api/auth", tags=["认证"])
app.include_router(users.router, prefix="/api/users", tags=["用户管理"])
app.include_router(customers.router, prefix="/api/customers", tags=["客户管理"])
app.include_router(products.router, prefix="/api/products", tags=["产品管理"])
app.include_router(sales.router, prefix="/api/sales", tags=["销售管理"])
app.include_router(production.router, prefix="/api/production", tags=["生产管理"])
app.include_router(procurement.router, prefix="/api/procurement", tags=["采购管理"])
app.include_router(warehouse.router, prefix="/api/warehouse", tags=["仓库管理"])
app.include_router(finance.router, prefix="/api/finance", tags=["财务管理"])

@app.get("/")
async def root():
    return {"message": "PrePy ERP API 服务正在运行", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "系统运行正常"}

if __name__ == "__main__":
    print(f"启动服务器，端口: {settings.PORT}")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.PORT,
        reload=True,
        log_level="info"
    )