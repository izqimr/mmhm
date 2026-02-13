import requests
import logging
from tenacity import retry, stop_after_attempt, wait_fixed
from common.yml import Yml


class Request:

    session = requests.Session()

    def __init__(self, env=None):
        self.env = env
        self.base_url = Yml().get_host()

    # ===============================
    # 重试机制（默认失败重试3次）
    # ===============================
    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def send(self,
             method,
             url,
             headers=None,
             params=None,
             data=None,
             json=None,
             files=None,
             timeout=5,
             need_token=False):

        full_url = self.base_url + url

        headers = headers or {}

        # ===============================
        # Token 注入（可扩展）
        # ===============================
        if need_token:
            token = self._get_token()
            headers["Authorization"] = f"Bearer {token}"

        # ===============================
        # 日志输出
        # ===============================
        logging.info("=" * 60)
        logging.info(f"请求方式: {method}")
        logging.info(f"请求地址: {full_url}")
        logging.info(f"请求头: {headers}")
        logging.info(f"请求params: {params}")
        logging.info(f"请求data: {data}")
        logging.info(f"请求json: {json}")

        try:
            response = self.session.request(
                method=method.upper(),
                url=full_url,
                headers=headers,
                params=params,
                data=data,
                json=json,
                files=files,
                timeout=timeout
            )

            logging.info(f"响应状态码: {response.status_code}")
            logging.info(f"响应内容: {response.text}")

            response.raise_for_status()  # 非2xx直接抛异常

            return response

        except requests.exceptions.RequestException as e:
            logging.error(f"请求异常: {e}")
            raise

    # ===============================
    # Token 获取逻辑（可重写）
    # ===============================
    def _get_token(self):
        """
        这里可以写登录接口获取 token
        也可以从缓存文件读取
        """
        return "your_token_here"

    # ===============================
    # 快捷方法封装
    # ===============================
    def get(self, url, **kwargs):
        return self.send("GET", url, **kwargs)

    def post(self, url, **kwargs):
        return self.send("POST", url, **kwargs)

    def put(self, url, **kwargs):
        return self.send("PUT", url, **kwargs)

    def delete(self, url, **kwargs):
        return self.send("DELETE", url, **kwargs)
