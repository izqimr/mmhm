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
        need_token=False,
    ):
        full_url = self.base_url + url
        headers = headers or {}

        if need_token:
            token = self._get_token()
            headers["Authorization"] = f"Bearer {token}"

        logger.info("=" * 60)
        logger.info("request method: %s", method)
        logger.info("request url: %s", full_url)
        logger.info("request headers: %s", headers)
        logger.info("request params: %s", params)
        logger.info("request data: %s", data)
        logger.info("request json: %s", json)

        try:
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

            logger.info("response status_code: %s", response.status_code)
            logger.info("response text: %s", response.text)

            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as exc:
            logger.error("request error: %s", exc)
            raise

    def _get_token(self):
        return "your_token_here"

    def get(self, url, **kwargs):
        return self.send("GET", url, **kwargs)

    def post(self, url, **kwargs):
        return self.send("POST", url, **kwargs)

    def put(self, url, **kwargs):
        return self.send("PUT", url, **kwargs)

    def delete(self, url, **kwargs):
        return self.send("DELETE", url, **kwargs)
