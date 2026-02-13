from common.yml import Yml
from common.auth import Auth
from common.request import Request

login = Auth()
re = Request()
y = Yml()

print(login.login())