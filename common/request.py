import requests
from tenacity import retry, stop_after_attempt, wait_fixed
from common.yml import Yml
from common.logger import get_logger

logger = get_logger(__name__)


class Request:
    session = requests.Session()

    def __init__(self, env=None):
        self.env = env
        self.base_url = Yml().get_host()

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def send(
        self,
        method,
        url,
        headers=None,
        params=None,
        data=None,
        json=None,
        files=None,
        timeout=5,
        need_token=True,
    ):
        base = self.base_url.rstrip("/")
        path = url.lstrip("/")
        full_url = f"{base}/{path}"
        headers = headers or {}

        if need_token:
            # Local import avoids circular dependency with Auth -> SupportApi -> Request.
            from common.auth import Auth

            token = Auth.get_token()
            headers["Authorization"] = f"Bearer {token}"

        logger.info("=" * 60)
        logger.info("method: %s", method)
        logger.info("url: %s", full_url)

        response = self.session.request(
            method=method.upper(),
            url=full_url,
            headers=headers,
            params=params,
            data=data,
            json=json,
            files=files,
            timeout=timeout,
        )

        logger.info("status_code: %s", response.status_code)
        logger.info("response: %s", response.text)

        # 自动刷新 token
        if response.status_code == 401 and need_token:
            logger.warning("token expired, refreshing...")
            from common.auth import Auth

            Auth.clear_token()
            token = Auth.get_token()
            headers["Authorization"] = f"Bearer {token}"
            response = self.session.request(
                method=method.upper(),
                url=full_url,
                headers=headers,
                params=params,
                data=data,
                json=json,
                files=files,
                timeout=timeout,
            )

        response.raise_for_status()
        return response

    def get(self, url, **kwargs):
        return self.send("GET", url, **kwargs)

    def post(self, url, **kwargs):
        return self.send("POST", url, **kwargs)

    def put(self, url, **kwargs):
        return self.send("PUT", url, **kwargs)

    def delete(self, url, **kwargs):
        return self.send("DELETE", url, **kwargs)
