# -*- coding: utf-8 -*-
from sql_app.database import Base, engine
from importlib import import_module


# 导入包
m = import_module("sql_app.models")

# 反射导入模型类（数据库表名），支持动态添加
# 为防止误操作，执行完一次后注释掉！！！
AuthInfo = getattr(m, "AuthInfo")


# 生成数据库表
Base.metadata.create_all(engine)
