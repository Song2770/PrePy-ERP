import os
import shutil
# 需要遍历的目录
root_dir = "./"
# 遍历目录
for dirpath, dirnames, filenames in os.walk(root_dir):
    if "__pycache__" in dirnames:
        # 获取 __pycache__ 目录的全路径
        pycache_dir = os.path.join(dirpath, "__pycache__")
        # 删除目录
        shutil.rmtree(pycache_dir)
        print(f"Removed: {pycache_dir}")
