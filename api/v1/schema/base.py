# -*- coding: utf-8 -*-
"""

[Schemas]
定义各类请求/响应体字段描述、约束、类型等

显式声明必需字段: 将默认参数的默认值设为 ... 三个省略号
声明非必需字段:   使用 Optional[] / Union[Any, None]，以及 Body 中的 default=None

"""


from typing import Any, Optional

from fastapi import Body
from pydantic import BaseModel


class TypeBaseResponse(BaseModel):
    code: int = Body(..., title='响应状态码', description='成功返回 0，失败为非 0', embed=True)
    msg: str = Body(..., title='响应描述说明', description='输出 success 或 failed，但不要以该值作为判断请求成功与否的依据', embed=True)
    data: Optional[Any] = Body(default=None, title='响应内容', description='返回可为空对象 null', embed=True)
