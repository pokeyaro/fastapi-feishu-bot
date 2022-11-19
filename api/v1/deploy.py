# -*- coding: utf-8 -*-
from typing import Dict

from asgiref.sync import sync_to_async
from fastapi.responses import Response
from fastapi import APIRouter, Depends

from common import logger
from schema.response import resp
from api.v1 import (
    authorize,
    TypeBaseResponse,
    TypeEventSubscription,
    TypeDeployMessage,
)
from feishu.api.send_msg import send_message


router = APIRouter()


@router.post(
    path="/event",
    summary="飞书事件初始订阅",
    name="event_subscribe",
    response_model=TypeEventSubscription,
)
async def event_subscribe(
        result: TypeEventSubscription
) -> Dict:
    logger.info(f'解析CHALLENGE值为: {result.challenge}')
    return result.dict()


@router.post(
    path="/notify",
    summary="部署类消息通知",
    name="deploy_notify",
    response_model=TypeBaseResponse,
)
async def deploy_notify(
        result: TypeDeployMessage,
        certify: str | None = Depends(authorize),
) -> Response:
    logger.info(f"认证token是: {certify}")
    context = result.data.dict()
    context['ip'] = str(result.data.ip).split('/')[0]
    for p in result.users:
        await sync_to_async(send_message)(p, **context)
    detail = "主机 {host} 任务已处理，通知 {count} 人：{name}".format(
        host=str(result.data.ip).split('/')[0],
        count=len(result.users),
        name=", ".join([str(p).split('@')[0] for p in result.users])
    )
    logger.info(detail)
    data = {"detail": detail}
    return resp.ok(data=data)
