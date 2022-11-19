import os
from typing import List, Optional
from pydantic import AnyHttpUrl, BaseSettings, DirectoryPath


class Settings(BaseSettings):
    # 开发模式配置
    DEBUG: bool = False

    # 项目文档名称
    TITLE: str = 'FastAPI Feishu Bot'

    # 项目文档描述
    DESCRIPTION: str = '该 FastAPI 项目主要提供飞书开放平台的机器人消息通知及 Hook 事件订阅等功能'

    # 版本
    VERSION: str = '1.0.0'

    # swagger 文档地址，默认为docs 生产环境关闭 None
    DOCS_URL: str = '/docs'

    # redoc 文档地址
    REDOC_URL: Optional[str] = '/redoc'

    # 文档关联请求数据接口
    OPENAPI_URL: str = '/openapi.json'

    # token过期时间 分钟
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    # 跨域设置 验证 list包含任意http url
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ['http://localhost']

    # 生成token的加密算法
    ALGORITHM: str = 'HS256'

    # 生产环境保管好 SECRET_KEY
    SECRET_KEY: str = '(-ASp+_)-Ulhw0848hnvVG-iqKyJSD&*&^-H3C9mqEqSl8KN-YRzRE'

    # 项目根路径
    BASE_PATH: DirectoryPath = os.path.dirname(os.path.dirname(os.path.dirname((os.path.abspath(__file__)))))


settings = Settings()
