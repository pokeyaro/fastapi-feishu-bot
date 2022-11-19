# -*- coding: utf-8 -*-
from sqlalchemy import Column, String, Integer, Boolean, DateTime, func

from .database import Base


class AuthInfo(Base):
    # 表的名字
    __tablename__ = 't-authinfo'

    # 表的结构
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(16), unique=True, nullable=False, comment='登录名')
    encrypted_password = Column(String(256), unique=True, nullable=False, comment='加密密码')
    dynamic_token = Column(String(512), comment='动态密钥')
    email = Column(String(64), unique=True, nullable=False, comment='电子邮箱')
    is_active = Column(Boolean(True), nullable=False, comment='是否激活')

    created_at = Column(DateTime, server_default=func.now(), comment='创建时间')
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='更新时间')

    def __repr__(self):
        return f"邮箱: {self.email}, 账号是否已被激活: {self.is_active}"

    @property
    def entry(self):
        return {
            'id': self.id,
            'username': self.username,
            'encrypted_password': self.encrypted_password,
            'email': self.email,
            'is_active': self.is_active,
            'ctime': self.created_at,
            'mtime': self.updated_at,
        }
