from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from typing import List
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="PrePy ERP API",
    description="Backend API for PrePy ERP System",
    version="0.1.0",
)

# Configure CORS
origins = os.getenv("APP_ALLOW_ORIGINS", '["http://localhost:3000", "http://127.0.0.1:3000"]')
if isinstance(origins, str):
    import json
    origins = json.loads(origins)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and include routers
from .app.api.v1.auth import router as auth_router
from .app.api.v1.users import router as users_router
from .app.api.v1.sales import router as sales_router
from .app.api.v1.technical import router as technical_router
from .app.api.v1.planning import router as planning_router
from .app.api.v1.dashboard import router as dashboard_router

# Add prefix to all API endpoints
api_prefix = "/api/v1"

# Include routers with prefix
app.include_router(auth_router, prefix=api_prefix)
app.include_router(users_router, prefix=api_prefix)
app.include_router(sales_router, prefix=api_prefix)
app.include_router(technical_router, prefix=api_prefix)
app.include_router(planning_router, prefix=api_prefix)
app.include_router(dashboard_router, prefix=api_prefix)

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to PrePy ERP API",
        "docs": "/docs",
        "redoc": "/redoc"
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Database check endpoint
@app.get("/api/v1/health/db-check")
async def db_health_check():
    try:
        # 添加数据库连接检查逻辑
        return {"status": "Database is healthy"}
    except Exception as e:
        return {"status": "Database is unhealthy", "error": str(e)}

if __name__ == "__main__":
    import logging
    import uvicorn
    logging.basicConfig(level=logging.INFO)
    logging.info('Backend service started successfully!')
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    print("Uvicorn Server started on port 8000")