"""
全局 Pytest 配置和 Fixtures
"""
import os
import sys
from pathlib import Path
import pytest
from common.logger import init_logger, get_logger
from common.auth import Auth
from common.request import Request
from common.db import DB

# 添加项目根目录到 Python 路径
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))


@pytest.fixture(scope="session", autouse=True)
def initialize_logger():
    """初始化日志（全局，自动执行）"""
    init_logger()
    logger = get_logger(__name__)
    logger.info("=" * 60)
    logger.info("测试框架初始化完成")
    logger.info("=" * 60)
    yield
    logger.info("=" * 60)
    logger.info("测试框架关闭")
    logger.info("=" * 60)


@pytest.fixture(scope="session")
def auth():
    """认证会话 fixture"""
    return Auth()


@pytest.fixture(scope="session")
def request_client():
    """HTTP 请求客户端 fixture"""
    return Request()


@pytest.fixture(scope="session")
def franchise_db():
    """Franchise 数据库连接 fixture"""
    return DB("franchise")


@pytest.fixture(scope="session")
def store_db():
    """Store 数据库连接 fixture"""
    return DB("store")


@pytest.fixture(scope="function")
def logger():
    """日志对象 fixture"""
    return get_logger(__name__)


# Pytest 钩子函数
def pytest_configure(config):
    """pytest 启动时的配置钩子"""
    pass


def pytest_collection_modifyitems(config, items):
    """修改收集到的测试项"""
    for item in items:
        # 为所有测试添加标记
        if "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        elif "unit" in str(item.fspath):
            item.add_marker(pytest.mark.unit)


@pytest.fixture(autouse=True)
def reset_db_after_test(request):
    """测试后重置数据库（如果需要）"""
    yield
    # 在此处添加测试后的清理逻辑
    # 例如: 删除测试中创建的数据
