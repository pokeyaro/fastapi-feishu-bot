# -*- coding: utf-8 -*-
from feishu.utils.http import StructRequest
from feishu.lark.auth import FeishuAccessToken


class LarkRequest(object):

    """
    携带飞书token进行请求处理
    """

    _token_instance = None

    def __init__(self, api: str, method: str, headers: dict = None, params: dict = None, payload: dict = None) -> None:
        # 域名地址
        self.host = 'https://open.feishu.cn'

        # Api资源路径
        self.api = api
        if self.api.endswith('/'):
            self.api = self.api[:-1]
        if not self.api.startswith('/'):
            self.api = '/' + self.api

        # 请求方式
        self.method = method.upper()

        # 设置请求参数
        if isinstance(params, dict):
            self.query_params = params
        else:
            self.query_params = None

        # 获取认证Token
        if self._token_instance is None:
            self._token_instance = FeishuAccessToken()
        token = self._token_instance.getter.get('tenant_access_token')

        # 添加额外的请求头
        self.request_headers = {
            'Authorization': 'Bearer {}'.format(token),
            'Content-Type': 'Content-Type: application/json; charset=utf-8',
        }
        if isinstance(headers, dict):
            for key, value in headers.items():
                if key not in ('Authorization', 'Content-Type'):
                    self.request_headers[key] = value

        # 设置请求体
        if isinstance(payload, dict):
            self.request_payload = payload
        else:
            self.request_payload = None

    @property
    def send(self) -> (dict, object):
        """ 构建HTTP请求 """
        r = StructRequest(host=self.host)
        dict_data, resp = r.send_request(
            path=self.api,
            method=self.method,
            headers=self.request_headers,
            params=self.query_params,
            body=self.request_payload,
        )
        # print(resp.headers['X-Tt-Logid'])       # For debug or oncall
        # print(resp.content)                     # Print Response
        return dict_data, resp                    # Has been json serialized
