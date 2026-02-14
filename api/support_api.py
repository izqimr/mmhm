from common.request import Request
from common.yml import Yml

class SupportApi:

    def __init__(self):
        self.yml = Yml()
        self.headers = self.yml.get_headers()


    def login(self, json):
        url = "/gateway/admin/user/login"
        return Request().post(url, json=json, headers=self.headers)
