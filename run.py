from common.auth import Auth
from common.request import Request
from common.yml import Yml
from common.logger import init_logger, get_logger

login = Auth()
re = Request()
y = Yml()


if __name__ == "__main__":
    init_logger()
    logger = get_logger(__name__)

    logger.info("start login flow")
    token = login.login()
    logger.info("login finished, token length=%s", len(token))

    print(token)
