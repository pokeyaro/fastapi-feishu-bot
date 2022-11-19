# -*- coding: utf-8 -*-
from typing import Any, Optional

from pydantic import BaseModel


# Pydantic orm_mode将告诉 Pydantic模型读取数据，
# 即它不是一个dict，而是一个 ORM 模型（或任何其他具有属性的任意对象）
# 错误：id = data["id"]
# 正确：id = data.id
class AuthInfo(BaseModel):
    id: int
    email: str
    username: str
    is_active: bool

    class Config:
        orm_mode = True


class AuthInDB(AuthInfo):
    encrypted_password: str
    dynamic_token: Optional[str]
    created_at: Any
    updated_at: Any
