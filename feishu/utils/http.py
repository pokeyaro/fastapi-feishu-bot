# -*- coding: utf-8 -*-
import json
import logging
import traceback

from urllib import parse
from typing import Dict, Union, Optional

import requests


class StructRequest(object):

    """
    对Request库的封装工具类：支持get和post请求
    """

    def __init__(self, host):
        self.host = host

    def _assembly_request_url(self, path: str, params: Optional[Dict[str, str]] = None) -> str:
        """
        描述: 组装完整的请求地址，请求参数需要通过字典来构建
        :param path: 请求路径（必填）
        :param params: 请求参数（非必填）
        :return: 请求完整url
        """
        if params is not None and isinstance(params, Dict):
            params_str = '?'
            for key, val in params.items():
                if val:
                    params_str += f'{key}={val}&'
            path = str(path + params_str)[:-1]
        return parse.urljoin(base=self.host, url=path)

    @staticmethod
    def _assembly_request_headers(headers: Optional[Dict] = None) -> Dict[str, any]:
        """ 设置请求头 """
        _data = {
            'Content-Type': 'application/json; charset=utf-8',
        }
        if headers is not None and isinstance(headers, dict):
            _data.update(headers)
        return _data

    @staticmethod
    def _assembly_request_payload(body: Optional[Dict] = None) -> str:
        """ 序列化请求体 """
        if body is not None and isinstance(body, dict):
            _data = json.dumps(body)
        else:
            _data = json.dumps({})
        return _data

    def send_request(
            self,
            path: str,
            method: str,
            headers: Optional[Dict] = None,
            params: Optional[Dict] = None,
            body: Optional[Dict] = None
    ) -> (Union[Dict[str, any], Exception], object):
        """
        描述: 发送HTTP请求
        :param path: 请求路径（必填）
        :param method: 请求方法（必填）
        :param headers: 请求头（非必填）
        :param params: 请求参数（非必填）
        :param body: 请求体（非必填）
        :return: 响应体, 响应对象
        """
        # 解析url (含请求参数)
        url = self._assembly_request_url(path, params)

        # 设置请求头
        _headers = self._assembly_request_headers(headers)

        # 根据不同类型进行请求
        method = method.lower()
        if method == 'get':
            r = requests.get(url=url, headers=_headers)
        elif method == 'post':
            _data = self._assembly_request_payload(body)
            r = requests.post(url=url, headers=_headers, data=_data)
        else:
            log = f'[http] method={method}, url={url}, body={body}, status_code=null, res=null'
            logging.error(log)
            raise ValueError("请求类型不支持")

        # 获取响应结果
        try:
            response = r.json()
        except Exception as e:
            log = f'[http] method={method}, url={url}, body={body}, status_code={r.status_code}, ' \
                  f'res={r.text}'
            logging.error(log)
            # Record the error log and throw it
            logging.error(str(e))
            logging.error(traceback.print_exc())
            raise e

        # 若未得到成功响应
        http_status_code = r.status_code
        if http_status_code != 200:
            err_code = response.get('code')
            err_msg = response.get('msg')
            log = f'[http] method={method}, url={url}, body={body}, status_code={r.status_code}, ' \
                  f'error_message={err_msg}, error_code={err_code}'
            logging.error(log)
            raise Exception(err_msg)

        return response, r
