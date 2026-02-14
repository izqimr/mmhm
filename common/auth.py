# common/auth.py
from email import header
from common.crypto import Crypto
from common.yml import Yml
from api.support_api import SupportApi


class Auth:

    def __init__(self):
        self.yml = Yml()

    def login(self):
        pwd = Crypto.encrypt(self.yml.get_password())
        data = {
            "appId": "sys_admin",
            "endpoint": "pc",
            "password": pwd,
            "userName": self.yml.get_username()
         }
        
        res = SupportApi().login(data)
        token = res.json()["data"]["token"]

        return token     