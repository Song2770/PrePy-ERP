from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from config import settings
import asyncpg

print("正在配置数据库连接...")

# 同步数据库引擎（用于初始化）
SYNC_DATABASE_URL = settings.DATABASE_URL.replace("postgresql://", "postgresql://")
engine = create_engine(SYNC_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 异步数据库引擎（用于API操作）
ASYNC_DATABASE_URL = settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
async_engine = create_async_engine(ASYNC_DATABASE_URL, echo=settings.DEBUG)
AsyncSessionLocal = sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)

# 数据库基类
Base = declarative_base()
metadata = MetaData()

# 依赖注入：获取数据库会话
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            print(f"数据库会话错误: {e}")
            await session.rollback()
            raise
        finally:
            await session.close()

# 创建数据库（如果不存在）
async def create_database_if_not_exists():
    """创建数据库（如果不存在）"""
    try:
        # 从DATABASE_URL中提取数据库信息
        import re
        url_pattern = r'postgresql://([^:]+):([^@]+)@([^:]+):([^/]+)/(.+)'
        match = re.match(url_pattern, settings.DATABASE_URL)
        
        if not match:
            raise ValueError("无效的数据库URL格式")
            
        username, password, host, port, database_name = match.groups()
        
        # 连接到postgres默认数据库来创建目标数据库
        admin_url = f"postgresql://{username}:{password}@{host}:{port}/postgres"
        
        print(f"正在检查数据库 '{database_name}' 是否存在...")
        
        # 使用asyncpg直接连接
        conn = await asyncpg.connect(admin_url)
        try:
            # 检查数据库是否存在
            result = await conn.fetchval(
                "SELECT 1 FROM pg_database WHERE datname = $1", database_name
            )
            
            if not result:
                print(f"数据库 '{database_name}' 不存在，正在创建...")
                # 创建数据库
                await conn.execute(f'CREATE DATABASE "{database_name}"')
                print(f"数据库 '{database_name}' 创建成功")
            else:
                print(f"数据库 '{database_name}' 已存在")
                
        finally:
            await conn.close()
            
    except Exception as e:
        print(f"创建数据库失败: {e}")
        raise

# 初始化数据库
async def init_db():
    try:
        # 首先确保数据库存在
        await create_database_if_not_exists()
        
        print("正在创建数据库表...")
        # 导入所有模型以确保它们被注册
        from models import (
            user, customer, product, sales, 
            production, procurement, warehouse, finance
        )
        
        # 创建所有表
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        
        print("数据库表创建完成")
        
        # 创建默认管理员用户
        await create_default_admin()
        
    except Exception as e:
        print(f"数据库初始化失败: {e}")
        raise

# 创建默认管理员用户
async def create_default_admin():
    from models.user import User
    from utils.auth import get_password_hash
    
    async with AsyncSessionLocal() as session:
        try:
            # 检查是否已存在管理员
            from sqlalchemy import select
            result = await session.execute(
                select(User).where(User.username == "admin")
            )
            admin_user = result.scalar_one_or_none()
            
            if not admin_user:
                print("正在创建默认管理员用户...")
                admin_user = User(
                    username="admin",
                    email="admin@prepy-erp.com",
                    hashed_password=get_password_hash("admin123"),
                    full_name="系统管理员",
                    is_active=True,
                    is_superuser=True
                )
                session.add(admin_user)
                await session.commit()
                print("默认管理员用户创建成功 (用户名: admin, 密码: admin123)")
            else:
                print("管理员用户已存在")
                
        except Exception as e:
            print(f"创建默认管理员失败: {e}")
            await session.rollback()