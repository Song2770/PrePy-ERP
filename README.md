# PrePy ERP
<img src="logo.png" alt="logo" align="center" />
PrePy ERP是一个基于Python和Vue.js的企业资源计划系统，旨在帮助企业管理销售、制造、采购和库存等日常业务流程。

## 系统架构

本系统采用前后端分离架构：

- 后端：FastAPI (Python)
- 前端：Vue 3 + Element Plus
- 数据库：PostgreSQL

## 主要功能模块

系统包含以下主要功能模块：

1. **销售管理**
   - 客户管理
   - 报价单管理
   - 销售订单管理
   - 发货管理
   - 发票管理

2. **计划管理**
   - 生产计划
   - 物料需求计划 (MRP)

3. **技术管理**
   - 产品管理
   - 物料清单 (BOM)
   - 工艺路线

4. **生产管理**
   - 工单管理
   - 生产跟踪
   - 工时记录

5. **采购管理**
   - 供应商管理
   - 采购订单
   - 来料检验

6. **仓库管理**
   - 库存管理
   - 入库管理
   - 出库管理
   - 库存盘点

7. **财务管理**
   - 应收账款
   - 应付账款
   - 费用管理

8. **系统管理**
   - 用户管理
   - 角色权限管理
   - 系统配置

## 项目结构

```
prepy-erp/
├── backend/                # 后端目录
│   ├── app/                # 主应用
│   │   ├── api/            # API路由
│   │   ├── config/         # 配置
│   │   ├── deps/           # 依赖项
│   │   ├── models/         # 数据模型
│   │   ├── schemas/        # Pydantic模式
│   │   └── utils/          # 工具函数
│   ├── main.py             # 主入口
│   └── setup_db.py         # 数据库初始化
│
├── frontend/               # 前端目录
│   ├── public/             # 静态资源
│   ├── src/                # 源代码
│   │   ├── api/            # API请求
│   │   ├── assets/         # 资源文件
│   │   ├── components/     # 公共组件
│   │   ├── layouts/        # 布局组件
│   │   ├── router/         # 路由配置
│   │   ├── store/          # 状态管理
│   │   ├── utils/          # 工具函数
│   │   └── views/          # 页面组件
│   ├── index.html          # HTML模板
│   └── vite.config.js      # Vite配置
│
└── README.md               # 项目说明
```

## 开发环境设置

### 后端

```bash
# 创建虚拟环境
python -m venv venv
venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 初始化数据库
python backend/setup_db.py

# 启动开发服务器
uvicorn backend.main:app  --reload
```

### 前端

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

## API文档

启动后端服务器后，可以访问以下地址查看API文档：

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 贡献

欢迎提交Pull Request或Issue来完善本项目。

## 许可证

本项目采用MIT许可证。 
