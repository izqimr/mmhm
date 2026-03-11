# common/auth.py
from common.crypto import Crypto
from common.yml import Yml
from api.support_api import SupportApi


class Auth:
    _token_cache = None

    def __init__(self):
        self.yml = Yml()

    def login(self):
        pwd = Crypto.encrypt(self.yml.get_password())
        data = {
            "appId": "sys_admin",
            "endpoint": "pc",
            "password": pwd,
            "userName": self.yml.get_username(),
        }

        res = SupportApi().login(data)
        token = res.json()["data"]["token"]
        if not token:
            raise Exception("Login failed: token missing")

        Auth._token_cache = token
        return token

    @classmethod
    def get_token(cls):
        if cls._token_cache:
            return cls._token_cache
        return cls().login()

    @classmethod
    def clear_token(cls):
        cls._token_cache = None
