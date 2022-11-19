# -*- coding: utf-8 -*-
"""

版本路由区分

路由支持添加所需要的依赖
https://fastapi.tiangolo.com/tutorial/bigger-applications/#import-fastapi

"""


from fastapi import APIRouter

from api.v1.home import router as home_router
from api.v1.deploy import router as deploy_router
from api.v1.oauth import router as oauth_router


api_v1_router = APIRouter()

api_v1_router.include_router(home_router, tags=["Home"])
api_v1_router.include_router(deploy_router, prefix="/api/v1/infra-delivery", tags=["Deploy"])
api_v1_router.include_router(oauth_router, prefix="/api/v1/oauth", tags=["OAuth2"])
