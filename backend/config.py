from pydantic_settings import BaseSettings
from typing import Optional
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # 数据库配置
    DATABASE_URL: str = "postgresql://postgres:PREPYsqladmin@localhost:5432/prepy_erp"
    
    # 服务器配置
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # JWT配置
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # 应用配置
    APP_NAME: str = "PrePy ERP"
    DEBUG: bool = True
    
    # 文件上传配置
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

# 确保上传目录存在
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

print(f"配置加载完成 - 数据库: {settings.DATABASE_URL}")
print(f"服务器将运行在: {settings.HOST}:{settings.PORT}")