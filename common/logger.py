# -*- coding: utf-8 -*-
"""

【FastAPI 中日志的配置】
在Python中内置了logging模块, 但是配置相对麻烦。
有人开发了一个日志扩展库loguru

【loguru 使用】
官方网站：    http://loguru.readthedocs.io/
Github地址： https://github.com/Delgan/loguru

【集成到 FastAPI】
原本是想，像flask那样把日志对象挂载到app对象上，作者建议直接使用全局对象
https://github.com/tiangolo/fastapi/issues/81#issuecomment-473677039
考虑是否应该把logger改成单例

【日志小技巧】
使用官方内置的库traceback能帮你更加详细的打印错误栈。
import traceback
logger.error(traceback.format_exc())

"""


import os
import time
from loguru import logger

from core.config import settings

# 定位到log日志文件
log_path = os.path.join(settings.BASE_PATH, 'logs')

if not os.path.exists(log_path):
    os.mkdir(log_path)

log_path_info = os.path.join(log_path, f'{time.strftime("%Y-%m-%d")}_info.log')
log_path_warning = os.path.join(log_path, f'{time.strftime("%Y-%m-%d")}_warning.log')
log_path_error = os.path.join(log_path, f'{time.strftime("%Y-%m-%d")}_error.log')

# 日志简单配置 文件区分不同级别的日志
logger.add(log_path_info, rotation="500 MB", encoding='utf-8', enqueue=True, level='INFO')
logger.add(log_path_warning, rotation="500 MB", encoding='utf-8', enqueue=True, level='WARNING')
logger.add(log_path_error, rotation="500 MB", encoding='utf-8', enqueue=True, level='ERROR')


__all__ = ["logger"]
