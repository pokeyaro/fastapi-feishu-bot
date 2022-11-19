# -*- coding: utf-8 -*-
from typing import Dict

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sql_app import get_auth_info
from utils import EncryptAES, token_signature, base64_encode, base64_decode


router = APIRouter()

# 请求Token的URL地址
oauth2_schema = OAuth2PasswordBearer(tokenUrl="/api/v1/oauth/token")


# 获取活跃用户字典信息
async def get_current_active_user(token: str = Depends(oauth2_schema)):
    data = base64_decode(token)
    if not isinstance(data, tuple):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},      # OAuth2的规范，如果认证失败，请求头中返回"WWW-Authenticate"
        )
    email, sign = data
    user_dict = get_auth_info(email=email)
    if not user_dict:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user_dict


# API
@router.options(path="/markdown", summary="说明手册", name="markdown")
def markdown():
    """
    ## 基于 Password 和 Bearer token 的简单 OAuth2 认证

    ### `OAuth2.0` 的四种授权模式
    - 授权码模式（`Authorization Code Grant`）
    - 隐式授权模式（`Implicit Grant`）
    - 密码授权模式（`Resource Owner Password Credentials Grant`）✅
    - 客户端凭证授权模式（`Client Credentials Grant`）

    ### 密码授权模式 - 流程图
    ```text
           User
    [Resource Owner]
           │
           │
           │   1. Authenticate with credentials
           │
           │                        2. Access token request
           ↓                  ——————————————————————————————————>
    [Client Application]                                               [Authorization Server]
                              <——————————————————————————————————
                                    3. Access token
    ```

    ### OAuth2PasswordRequestForm 是一个类依赖项，声明了如下的请求表单：
    - **username**: 必填
    - **password**: 必填
    - **scope**: 是一个由空格分隔的字符串组成的大字符串
    - **grant_type**: `OAuth2` 规范实际上要求 `grant_type` 字段使用一个固定的值 `password`，但是 `OAuth2PasswordRequestForm` 未强制约束
    - **client_id**: 可选的
    - **client_secret**: 可选的

    ### FastAPI 的 OAuth2PasswordBearer 类
    ```text
    OAuth2PasswordBearer 是接收 URL 作为参数的一个类：客户端会向该 URL 发送 username 和 password 参数，然后得到一个 Token 值。

    OAuth2PasswordBearer 并不会创建相应的 URL 路径操作，只是指明客户端用来请求 Token 的 URL 地址。

    当请求到来的时候，FastAPI 会检查请求的 Authorization 头信息，如果没有找到 Authorization 头信息，
    或者头信息的内容不是 Bearer Token，它会返回 401 状态码（UNAUTHORIZED）
    ```
    """
    return None


# 时间签名，动态token设计思路
# encrypt_passwd = encrypt(password)
# username + encrypt_passwd -> db , 匹配到数据则进行颁发签名
# sha256(username + encrypt_passwd + timestamp) 对比两次执行的结果，若结果一致，则认证通过；反之认证失败
@router.post(path="/token", summary="请求认证", name="login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Dict:
    # 前端获取数据
    username = form_data.username
    password = form_data.password
    # 数据加密
    encrypt_passwd = EncryptAES().encode_aes(password)
    # 检查是否在数据库中
    user_dict = get_auth_info(username=username, password=encrypt_passwd)
    if not user_dict:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password")
    # 查看email
    email = user_dict.get('email')
    # 设置token
    token = token_signature(username=username, password=encrypt_passwd)
    # 返回最终值
    res = base64_encode(email, token)
    return {"access_token": res, "token_type": "bearer"}


@router.get(path="/bearer", summary="密钥测试", deprecated=True)
async def bearer(token: str = Depends(oauth2_schema)) -> Dict:
    return {"token": token}


@router.get("/whoami", summary="我是谁")
async def whoami(current_user: Dict = Depends(get_current_active_user)):   # 依赖注入系统
    user = current_user.get('email').split('@')[0]
    return user
