# -*- coding: utf-8 -*-
import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# 建立数据库连接
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db_name"
# python3+ 版本依赖 mysql 客户端 pip install pymysql

# 生产环境/开发环境
env_db_user = os.getenv('DB_USER')
env_db_passwd = os.getenv('DB_PASSWD')
env_db_host = os.getenv('DB_HOST')
env_db_port = os.getenv('DB_PORT')
env_db_name = os.getenv('DB_NAME')
if env_db_user and env_db_passwd and env_db_host and env_db_port and env_db_name:
    SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{env_db_user}:{env_db_passwd}@{env_db_host}:{env_db_port}/{env_db_name}"
else:
    SQLALCHEMY_DATABASE_URL = "mysql+pymysql://***"


# echo=True表示引擎将用repr()函数记录所有语句，以及参数列表到日志。
# 由于SQLAlchemy是多线程，指定check_same_thread=False来让建立的对象任意线程都可以使用。
# 默认情况下，SQLite 只允许一个线程与其通信，假设有多个线程的话，也只将处理一个独立的请求。
# 仅用于SQLite，在其他数据库不需要它。
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    encoding='utf-8',
    echo=True,
    max_overflow=5,
    # connect_args={'check_same_thread': False}
)

# 在SQLAlchemy中，Crud都是通过会话（session）进行的，所以我们必须要先创建会话，每一个SessionLocal实例都是一个数据库session。
# flush()是指发送sql语句到数据库，但不一定落盘；commit()提交事务，将变更保存到数据库文件
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=True)

# 创建基本的映射类 (orm基类)
Base = declarative_base(bind=engine, name='Base')
