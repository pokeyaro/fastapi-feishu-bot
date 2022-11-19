# -*- coding: utf-8 -*-
import time
import base64
import hashlib


def token_signature(username: str, password: str) -> str:
    """
    时间戳去掉整数部分的后四位，即最长9999s，token最长2h就要更换
    :param username:
    :param password:
    :return:
    """
    occur_time = time.time()
    deadline_timestamp = "{:.0f}".format(occur_time)[:-4] + "0" * 4
    # 构建时间签名
    data = username + password + deadline_timestamp
    result = hashlib.sha256(data.encode('utf-8')).hexdigest()
    return result


def base64_encode(email: str, token: str) -> str:
    """ 加密 """
    data = email + '$$' + token
    secret_str = base64.b64encode(data.encode('utf-8')).decode()
    return secret_str


def base64_decode(data: str):
    """ 解密 """
    result = base64.b64decode(data.encode('utf-8')).decode()
    string = result.split('$$')
    email = string[0]
    token = string[1]
    return email, token
