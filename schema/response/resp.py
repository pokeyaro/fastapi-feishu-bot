# -*- coding: utf-8 -*-
"""

统一响应状态码

"""

from enum import Enum
from typing import Union

from fastapi import status as http_status
from fastapi.responses import JSONResponse, Response
from fastapi.encoders import jsonable_encoder


class Msg(str, Enum):
    success = "success"
    failed = "failed"


class Resp(object):
    def __init__(self, code: int, detail: str, status: int):
        self.code = code
        self.detail = detail
        self.status = status

    def set_msg(self, detail):
        self.detail = detail
        return self


InvalidRequest: Resp = Resp(10001, "无效的请求", http_status.HTTP_400_BAD_REQUEST)
InvalidParams: Resp = Resp(10002, "无效的参数", http_status.HTTP_400_BAD_REQUEST)
BusinessError: Resp = Resp(10003, "业务错误", http_status.HTTP_400_BAD_REQUEST)
DataNotFound: Resp = Resp(10004, "查询失败", http_status.HTTP_400_BAD_REQUEST)
DataStoreFail: Resp = Resp(10005, "新增失败", http_status.HTTP_400_BAD_REQUEST)
DataUpdateFail: Resp = Resp(10006, "更新失败", http_status.HTTP_400_BAD_REQUEST)
DataDestroyFail: Resp = Resp(10007, "删除失败", http_status.HTTP_400_BAD_REQUEST)
AccessDenied: Resp = Resp(10008, "访问遭拒绝", http_status.HTTP_400_BAD_REQUEST)
PermissionDenied: Resp = Resp(10009, "权限拒绝", http_status.HTTP_403_FORBIDDEN)
ServerError: Resp = Resp(50000, "服务器繁忙", http_status.HTTP_500_INTERNAL_SERVER_ERROR)


def ok(*, data: Union[list, dict] = None) -> Response:
    return JSONResponse(
        status_code=http_status.HTTP_200_OK,
        content=jsonable_encoder({
            'code': 0,
            'msg': Msg.success.value,
            'data': data
        })
    )


def fail(resp: Resp) -> Response:
    return JSONResponse(
        status_code=resp.status,
        content=jsonable_encoder({
            'code': resp.code,
            'msg': Msg.failed.value,
            'detail': resp.detail
        })
    )
