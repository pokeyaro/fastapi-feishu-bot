# -*- coding: utf-8 -*-
"""

通过依赖注入进行引用

"""


from typing import Optional, List

from fastapi import Header, HTTPException, status

from common import logger
from sql_app import get_auth_info
from utils import token_signature, base64_decode


async def authorize(
        authorization: Optional[List[str]] = Header(default=None)
):
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},      # OAuth2的规范，如果认证失败，请求头中返回"WWW-Authenticate"
        )
    token = str(authorization).replace('Bearer ', '')
    user_dict, email = None, None
    try:
        data = base64_decode(token)
        email, sign = data
        user_dict = get_auth_info(email=email)
    except Exception:
        pass
    if not user_dict:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    username = user_dict.get('username')
    encrypt_passwd = user_dict.get('encrypted_password')
    validation_value = token_signature(username=username, password=encrypt_passwd)
    logger.info(f"当前登录用户为: {email}, 已授权通过！")
    return validation_value
