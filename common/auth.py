# common/auth.py
from email import header
from common.crypto import Crypto
from common.request import Request
from common.yml import Yml
from api.support_api import SupportApi


class Auth:

    # def login(self) -> str:
    #     """
    #     登录并返回 token
    #     """
    #     req = Request()
    #     yml = Yml()
    #     # 加密
    #     pwd = Crypto.encrypt(yml.get_password())
    #     url = "/gateway/admin/user/login"
    #     header = yml.get_header()

    #     data = {
    #         "appId": "sys_admin",
    #         "endpoint": "pc",
    #         "password": pwd,
    #         "userName": yml.get_username()
    #     }

    #     resp = req.post(url=url, json=data, headers=header)
    #     token = resp.json()["data"]["token"]

    #     return token
    def __init__(self):
        self.yml = Yml()

    def login(self):
        pwd = Crypto.encrypt(self.yml.get_password())
        header = self.yml.get_header()
        data = {
             "appId": "sys_admin",
             "endpoint": "pc",
             "password": pwd,
            "userName": self.yml.get_username()
         }
        
        res = SupportApi().login(data)
        token = res.json()["data"]["token"]

        return token 