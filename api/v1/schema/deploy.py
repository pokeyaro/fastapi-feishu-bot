# -*- coding: utf-8 -*-
from typing import Set

from fastapi import Body
from pydantic import BaseModel, IPvAnyNetwork


class TypeEventSubscription(BaseModel):
    challenge: str = Body(..., title='挑战值', description='应用需要在响应中原样返回的值', embed=True)
    token: str = Body(..., title='认证 Token', description='即 Verification Token', embed=True)
    type: str = Body(..., title='请求类型', description='表示这是一个验证请求', embed=True)


class TypeDeployCard(BaseModel):
    ip: IPvAnyNetwork = Body(..., title='目标主机', description='仅支持 IPv4 地址', embed=True)
    title: str = Body(..., title='消息卡片标题', max_length=32, embed=True)
    content: str = Body(..., title='消息卡片内容', description='支持多行文本，使用 \\n 换行', max_length=512, embed=True)
    color: str = Body(default='Blue', title='消息卡片背景颜色', description='非必填，可选值为: "Red", "Blue"', embed=True)


class TypeDeployMessage(BaseModel):
    users: Set[str] = Body(..., title='卡片接收用户', embed=True)
    data: TypeDeployCard = Body(..., title='卡片消息主体', embed=True)
