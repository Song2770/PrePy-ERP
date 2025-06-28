# 路由模块初始化文件
print("正在初始化路由模块...")

# 导入所有路由模块
from . import auth
from . import users
from . import customers
from . import products
from . import sales
from . import production
from . import procurement
from . import warehouse
from . import finance

print("路由模块初始化完成")