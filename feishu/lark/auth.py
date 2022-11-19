# -*- coding: utf-8 -*-
"""

【自建应用获取 tenant_access_token】

tenant_access_token 的最大有效期是 2 小时 (7200s)。
如果在有效期小于 30 分钟 (1800s) 的情况下，调用本接口，会返回一个新的 tenant_access_token，这会同时存在两个有效的 tenant_access_token

响应体示例
{
    'code': 0,
    'expire': 7200,                                                       // 过期时间，单位为秒
    'msg': 'ok',
    'tenant_access_token': 't-g104bbno7LHWM5S2NVPE7SHCJEXQGNCP6SVK5VCY'   // 租户访问凭证
}

"""

import os
import time
import json
import logging
import traceback

from importlib import import_module
from typing import Dict, Union, Optional
from datetime import datetime, timedelta

import requests


def get_app_info() -> Dict[str, str]:

    """
    获取飞书APP应用凭证信息
    :return:
    """

    define_user = 'APP_ID'
    define_passwd = 'APP_SECRET'

    env_app_id = os.getenv(define_user)
    env_app_secret = os.getenv(define_passwd)

    if env_app_id and env_app_secret:
        # 生产环境
        data = {
            'app_id': env_app_id,
            'app_secret': env_app_secret,
        }
    else:
        # 开发环境
        try:
            path = "tests.local_settings"
            module = import_module(path)
            data = {
                'app_id': getattr(module, define_user),
                'app_secret': getattr(module, define_passwd),
            }
        except ImportError as e:
            logging.error(str(e))
            logging.error(traceback.print_exc())
            raise e

    return data


class FeishuAccessToken(object):

    """
    处理飞书开放平台，自建应用获取token的封装类
    """

    __author__ = 'Mystic'

    # 定义一个类变量 getter
    getter: Dict[str, Union[str, datetime.timestamp, None]] = {
        'expire_timestamp': None,
        'tenant_access_token': None,
        'message': None,
    }

    # 定义登记的app账号
    _account: Dict[str, str] = dict()

    def __init__(self, app_id: Optional[str] = None, app_secret: Optional[str] = None):
        """
        若token未到期，不会向飞书服务器发送新的请求，将从getter中直接读取数据
        :param app_id:
        :param app_secret:
        """
        if app_id is None and app_secret is None:
            _app_ticket = self._account
        else:
            _app_ticket = {
                "app_id": app_id,
                "app_secret": app_secret
            }
            self._account.update(_app_ticket)
        self._app_ticket = json.dumps(_app_ticket)

        if self.getter['expire_timestamp'] is None:
            # 初始化逻辑
            self._mount_expiration()
        else:
            # 后续实例化走这里
            self._check_expired()

    @property
    def _timestamp_fmt_string(self) -> str:
        """
        时间戳转化为格式化时间字符串的方法
        :return:
        """
        ts = self.getter["expire_timestamp"]
        date_format = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ts))
        return date_format

    @property
    def _get_tenant_access_token(self) -> Dict[str, Union[str, int]]:
        """
        向飞书服务器发起请求，获取应用的通行凭证tenant_access_token，
        并将该token赋值给getter类变量
        :return:
        """
        url = 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal'
        method = 'POST'
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
        }
        resp = requests.request(url=url, method=method, headers=headers, data=self._app_ticket)
        try:
            resp = resp.json()
        except Exception as e:
            logging.error(str(e))
            logging.error(traceback.print_exc())
            raise e
        self.getter.update({
            'tenant_access_token': resp.get('tenant_access_token')
        })
        return resp

    def _mount_expiration(self) -> None:
        """
        将过期时间戳挂载到getter类变量中
        :return:
        """
        valid_sec = self._get_tenant_access_token.get('expire') - (30 * 60)
        self.getter.update({
            'expire_timestamp': (datetime.now() + timedelta(seconds=valid_sec)).timestamp()
        })

    def _check_expired(self) -> None:
        """
        通过getter类变量的过期时间戳与当前时间进行比较，来检查token是否过期，
        若过期，则向飞书服务器重新发起请求，获取最新的token，
        若没过期，则继续使用getter类变量中的token值。
        :return:
        """
        if self.getter['expire_timestamp'] > datetime.now().timestamp():
            info = 'The current token is available, and the expiration time is'
        else:
            # 因认证过期，重新获取token
            self._mount_expiration()
            info = 'The latest token has been refreshed, and the expiration time is'
        self.getter.update({
            'message': '{}: {}'.format(info, self._timestamp_fmt_string)
        })


# 获取APP凭证
conf = get_app_info()

# 首次初始化对象
initial = FeishuAccessToken(**conf)

# 只允许导出 FeishuAccessToken 类
__all__ = ["FeishuAccessToken"]


# 测试
if __name__ == '__main__':
    t1 = FeishuAccessToken()
    print(t1.getter)
    t2 = FeishuAccessToken()
    print(t2.getter)
