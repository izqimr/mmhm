"""
主运行脚本 - 用于快速启动测试
"""
import os
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

from common.logger import init_logger, get_logger

if __name__ == "__main__":
    init_logger()
    logger = get_logger(__name__)
    
    logger.info("=" * 60)
    logger.info("自动化测试框架启动")
    logger.info("=" * 60)
    
    # 推荐使用 pytest 命令行运行：
    # python -m pytest tesecase/franchise/test_create_store.py -v
    # 或直接运行：
    # pytest tesecase/franchise/ -v
    
    logger.info("请使用 pytest 命令来运行测试")
    logger.info("更多信息请查看 README.md")


    