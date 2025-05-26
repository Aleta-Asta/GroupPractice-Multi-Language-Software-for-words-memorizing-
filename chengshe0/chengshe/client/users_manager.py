
import json
import os
from typing import Dict

# 获取数据文件路径
_DATA_DIR = os.path.dirname(os.path.abspath(__file__))
USER_DATA_PATH = os.path.join(_DATA_DIR, "../user/users.json")

def load_users() -> Dict[str, str]:
    """加载用户数据，文件不存在时创建默认数据"""
    if not os.path.exists(USER_DATA_PATH):
        default_data = {"admin": "admin123"}
        save_users(default_data)
    try:
        with open(USER_DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {"让三颗心免于哀伤": "114514"}  # 文件损坏时返回默认数据

def save_users(users: Dict[str, str]) -> None:
    """保存用户数据到文件"""
    with open(USER_DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2, ensure_ascii=False)

# 初始化加载数据
users = load_users()