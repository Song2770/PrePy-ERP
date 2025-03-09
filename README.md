# PrePy ERP System

一个全面的企业资源规划（ERP）系统，使用Python后端，Vue.js前端和PostgreSQL数据库。

## 系统架构

- **后端**: FastAPI (Python)
- **前端**: Vue.js 3 + Vite
- **数据库**: PostgreSQL
- **ORM**: SQLAlchemy
- **迁移工具**: Alembic
- **任务队列**: Celery + Redis

## 系统模块

1. **销售管理** - 从报价到收款的全流程管理
2. **技术管理** - 产品设计、BOM管理和技术准备
3. **计划管理** - 生产计划、物料需求计划(MRP)
4. **生产管理** - 生产执行和质量控制
5. **采购管理** - 供应商管理和采购流程
6. **库存管理** - 库存监控和物料流转
7. **财务管理** - 财务核算和分析
8. **供应链管理** - 供应链优化和分析
9. **客户关系管理** - 客户信息管理和服务
10. **人力资源管理** - 员工管理、考勤和绩效
11. **技术与数据分析** - 业务数据分析和决策支持

## 开发环境设置

### 后端设置

1. 创建虚拟环境:
```bash
python -m venv venv
```
```bash
venv\Scripts\activate  # Windows
```
```bash
source venv/bin/activate  # Linux/MacOS
```

2. 安装依赖:
```bash
pip install -r requirements.txt
```

3. 设置环境变量:
复制 `.env.example` 到 `.env` 并配置环境变量。

4. 运行迁移:
```bash
alembic upgrade head
```

5. 启动开发服务器:
```bash
uvicorn backend.main:app --reload
```

### 前端设置

1. 安装依赖:
```bash
cd frontend
npm install
```

2. 启动开发服务器:
```bash
npm run dev
```

## API文档
~~
启动后端服务器后，可以在以下位置访问API文档:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
~~
## 数据库模式

详细的数据库模式文档位于 `database/schema.md`。

## 许可证

[MIT](LICENSE) 
