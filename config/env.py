"""
配置管理模块 - 环境变量加载和配置常量定义

此模块负责：
1. 加载 .env 文件到环境变量
2. 定义配置常量供其他模块导入
3. 处理类型转换和默认值

环境变量加载优先级：
1. ENVIRONMENT 系统环境变量 (指定环境，如 test/pre/prod)
2. .env.{ENVIRONMENT} 文件 (如 .env.test)
3. .env 文件 (本地开发配置)
4. 默认值 (test 环境)

使用示例：
    from config.env import HOST, USERNAME, FRANCHISE_DB_HOST
    print(f"Host: {HOST}, User: {USERNAME}")
"""
from pathlib import Path
import os
from dotenv import load_dotenv

# =============================================================================
# 环境变量加载逻辑
# =============================================================================

# 环境切换逻辑
# 优先级：OS环境变量 > 本地 .env > 默认值(test)
_env_name = os.getenv("ENVIRONMENT", "test")

# 按优先级加载 .env 文件
# 优先级：本地.env > 环境特定.env (如 .env.test)
base_dir = Path(__file__).resolve().parent.parent
env_files = [
    base_dir / f".env.{_env_name}",  # 例如: .env.test
    base_dir / ".env",                # 本地开发配置
]

for env_file in env_files:
    if env_file.exists():
        load_dotenv(dotenv_path=env_file, override=True)
        break

# =============================================================================
# 基础路径配置
# =============================================================================

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"
LOG_FILE = LOG_DIR / os.getenv("LOG_FILE_NAME", "framework.log")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

# =============================================================================
# 应用配置（从环境变量读取）
# =============================================================================

# 环境标识
APP_ENV = os.getenv("ENV", "test")

# API 配置
HOST = os.getenv("HOST", "")
USERNAME = os.getenv("USERNAME", "")
PASSWORD = os.getenv("PASSWORD", "")
APP_ID = os.getenv("APP_ID", "")
APP_SECRET = os.getenv("APP_SECRET", "")

# =============================================================================
# 数据库配置
# =============================================================================

#招商数据库配置
FRANCHISE_DB_HOST = os.getenv("FRANCHISE_DB_HOST", "")
FRANCHISE_DB_USER = os.getenv("FRANCHISE_DB_USER", "")
FRANCHISE_DB_PASSWORD = os.getenv("FRANCHISE_DB_PASSWORD", "")
FRANCHISE_DB_PORT = int(os.getenv("FRANCHISE_DB_PORT", "3306"))
FRANCHISE_DATABASE = os.getenv("FRANCHISE_DATABASE", "")

# 门店数据库配置
STORE_DB_HOST = os.getenv("STORE_DB_HOST", "")
STORE_DB_USER = os.getenv("STORE_DB_USER", "")
STORE_DB_PASSWORD = os.getenv("STORE_DB_PASSWORD", "")
STORE_DB_PORT = int(os.getenv("STORE_DB_PORT", "3306"))
STORE_DATABASE = os.getenv("STORE_DATABASE", "")
