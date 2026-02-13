from common.request import Request
from common.yml import Yml

class SupportApi:

    def __init__(self):
        self.yml = Yml()
        self.header = self.yml.get_header()


    def login(self, json):
        url = "/gateway/admin/user/login"
        return Request.post("post", url, json=json, header=self.header)