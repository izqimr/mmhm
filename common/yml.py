# common/yml.py
import os
from config.env import (
    HOST, USERNAME, PASSWORD, APP_ID, APP_SECRET,
    FRANCHISE_DB_HOST, FRANCHISE_DB_USER, FRANCHISE_DB_PASSWORD, FRANCHISE_DB_PORT, FRANCHISE_DATABASE,
    STORE_DB_HOST, STORE_DB_USER, STORE_DB_PASSWORD, STORE_DB_PORT, STORE_DATABASE
)
import yaml


class Yml:
    """
    配置管理类 - 从环境变量读取配置
    
    所有敏感信息和环境相关配置已迁移到 .env 文件
    此类负责读取 .env 中的配置和 data/ 目录下的测试数据文件
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        """单例模式"""
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """初始化配置"""
        if hasattr(self, "_initialized"):
            return
        self._initialized = True
    
    def get_host(self):
        """获取 API 主机地址"""
        return HOST
    
    def get_username(self):
        """获取用户名"""
        return USERNAME
    
    def get_password(self):
        """获取密码"""
        return PASSWORD
    
    def get_franchiseDB_info(self):
        """获取 Franchise 数据库连接信息"""
        return {
            "DB_host": FRANCHISE_DB_HOST,
            "DB_user": FRANCHISE_DB_USER,
            "DB_password": FRANCHISE_DB_PASSWORD,
            "DB_port": FRANCHISE_DB_PORT,
            "DataBase": FRANCHISE_DATABASE,
        }
    
    def get_storeDB_info(self):
        """获取 Store 数据库连接信息"""
        return {
            "DB_host": STORE_DB_HOST,
            "DB_user": STORE_DB_USER,
            "DB_password": STORE_DB_PASSWORD,
            "DB_port": STORE_DB_PORT,
            "DataBase": STORE_DATABASE,
        }
    
    def get_headers(self):
        """获取请求头"""
        return {
            "Content-Type": "application/json",
            "x-app-id": APP_ID,
            "X-App-Secret": APP_SECRET,
        }

    def read_yaml(self, file_path):
        """
        读取 YAML 测试数据文件
        
        Args:
            file_path: 测试数据文件路径（如 data/franchise/create_store.yml）
            
        Returns:
            解析后的 YAML 数据（字典或列表）
        """
        with open(file_path, encoding="utf-8") as f:
            return yaml.safe_load(f)
