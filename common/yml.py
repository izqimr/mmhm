# common/config.py
import os
import yaml

class Yml:

    # def __init__(self):
    #     # 获取项目根目录
    #     root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace('\\', '/')
    #     # 拼接配置文件目录
    #     conf_dir = root_dir + '/' + 'config/config.yml'

    #     # 读取 yaml 文件
    #     with open(conf_dir, 'r', encoding='utf-8') as f:
    #         self.data = yaml.safe_load(f)

    #     # 读取环境变量，默认 test
    #     self.env = os.environ.get("API_ENV", "test")

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, "_initialized"):
            return

        root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace('\\', '/')
        conf_path = os.path.join(root_dir, "config", "config.yml")

        with open(conf_path, 'r', encoding='utf-8') as f:
            self.data = yaml.safe_load(f)

        self.env = os.environ.get("API_ENV", "test")
        self._initialized = True
    
    def get_host(self):
        return self.data["envs"][self.env]["public"]["host"]
    
    def get_username(self):
        return self.data["envs"][self.env]["public"]["username"]
    
    def get_password(self):
        return self.data["envs"][self.env]["public"]["password"]
    
    def get_franchiseDB_info(self):
        return self.data["envs"][self.env]["franchiseDB"]
    
    def get_storeDB_info(self):
        return self.data["envs"][self.env]["storeDB"]
    
    def get_headers(self):
        return self.data["envs"][self.env]["public"]["headers"]