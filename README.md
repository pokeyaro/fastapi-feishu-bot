# FastAPI + MySQL - 搭建飞书消息模块

## 概述

> 一个异步的 `Web` 开发框架，它不同于 `Django` 或 `Flask` 的同步框架; 自带 `swagger` / `redoc` API 文档; 独特的**依赖注入系统**...

初体验 `FastAPI` 框架，
参考 [FastAPI官网](https://fastapi.tiangolo.com/tutorial) 示例代码，
和 [fastapi-mysql-generator项目](https://github.com/wxy2077/fastapi-mysql-generator) 大部分代码。

## 功能介绍

**1. `Swagger API` 文档**

![image](https://user-images.githubusercontent.com/58482090/202836719-40547259-ef12-4d83-a81d-c83fdb96695f.png)

**2. `Token` 认证**

![image](https://user-images.githubusercontent.com/58482090/202837456-b5fcfd52-c5ae-440a-a616-cfe3fdddeb52.png)

**3. 发送飞书消息** (动态 `token` 添加到 `Header` 中)

![image](https://user-images.githubusercontent.com/58482090/202838474-1026466d-92d1-4c09-a440-22b4842f93fd.png)

**4. 效果预览**

![image](https://user-images.githubusercontent.com/58482090/202838353-c33a7eb9-a17f-4df2-8f9c-2a44fd720035.png)



## 关键点

- 依赖注入系统
- Schemas模式（Pydantic）
- SQLAlchemy的ORM操作(Pymysql)
- Typing hint类型提示
- 统一的Restful响应体风格
- Loguru日志集成配置
- Oauth2密码认证模式
- Requests的二次封装


## 生产部署

```shell
cd project_dir/
# 安装依赖库
pip install -r requirements.txt

# 使用ASGI协议框架 - 使用 Uvicorn 异步服务启动 (可搭配supervisor托管后台运行)
uvicorn main:app --host=127.0.0.1 --port=8000 --reload
uvicorn main:app --host=127.0.0.1 --port=8000 --workers=4
```


## 如何集成

- 注入ENV环境变量：
```text
准备一个飞书应用账号
---
APP_ID='cli_a3c*******73c900c'
APP_SECRET='JkDGAVj3p3z************uLR3i683'

准备一个MysqlDB服务器
---
DB_USER='root'
DB_PASSWD='*****'
DB_HOST='127.0.0.1'
DB_PORT='3306'
DB_NAME='app'
```

- 初始化数据库：
```text
需对库进行migrate操作（生成表）：
# ./venv/bin/python3 sql_app/operation/migrate.py

添加一条oauth2用户数据条目（建议使用脚本，密码字段为密文）：
# ./venv/bin/python3 sql_app/operation/create_user.py

当然也可以使用sql，初始化sql脚本：
# mysql -uroot -p***** < initial.sql
```


## 项目目录

```shell
.
├── README.md                              # 自述文件
├── api                                    # api目录
│   ├── __init__.py
│   └── v1
│       ├── __init__.py
│       ├── depend
│       │   └── verify_header.py
│       ├── deploy.py                     # 功能api
│       ├── home.py
│       ├── oauth.py
│       └── schema                        # 各功能api相对应的schema类型目录
│           ├── base.py
│           ├── deploy.py
│           └── oauth.py
├── common                                 # 功能函数
│   ├── __init__.py
│   ├── custom_exc.py                     # 自定义异常
│   └── logger.py                         # 日志模块
├── core                                   # 核心目录
│   ├── config                            # 项目配置
│   │   ├── __init__.py
│   │   ├── development_config.py
│   │   └── production_config.py
│   └── server.py                         # 挂载app对象
├── feishu                                 # 飞书业务代码相关
│   ├── api                               # api目录
│   │   └── send_msg.py
│   ├── lark                              # lark平台认证及消息卡片模板
│   │   ├── auth.py
│   │   └── card.py
│   └── utils                             # 封装通用requests库请求
│       ├── http.py
│       └── wrapper.py
├── logs                                   # 本地日志
│   ├── 2022-11-17_error.log
│   ├── 2022-11-17_info.log
│   └── 2022-11-17_warning.log
├── main.py                                # 主入口文件
├── requirements.txt                       # 依赖说明
├── router                                 # 路由系统
│   └── v1_router.py
├── schema                                 # 通用模式类型
│   └── response
│       └── resp.py                       # 统一的响应体格式
├── sql_app                                # sqlalchemy相关ORM目录
│   ├── __init__.py
│   ├── crud.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── operation                          # 迁移脚本等
│   │   ├── create_user.py
│   │   ├── initial.sql
│   │   └── migrate.py
│   └── schemas.py
├── static                                 # 静态文件（不涉及）
├── tests                                  # 本地测试目录
│   └── local_settings.py
└── utils                                  # 工具类
    ├── __init__.py
    ├── crypts.py
    └── tickets.py
```


## 历史版本

之前使用 `Flask` 的蓝图布局，写过一个简单版本的飞书机器人消息 `API Restful` 服务：
[仓库地址](https://github.com/PokeyBoa/lark-robot-message)
