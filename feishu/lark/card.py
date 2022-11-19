# -*- coding: utf-8 -*-
"""

飞书开放平台 - 消息卡片搭建工具
https://open.feishu.cn/tool/cardbuilder

"""

import json
from enum import Enum
from datetime import datetime


class ColorStyle(str, Enum):
    red = "Red"
    blue = "Blue"
    green = "Green"
    yellow = "Yellow"


class TemplateCard:

    def __init__(self):
        self.card = None

    @property
    def to_json(self) -> str | TypeError:
        """ 转换为json格式 """
        if isinstance(self.card, dict):
            return json.dumps(self.card)
        else:
            raise TypeError("Only accepts dict type!")

    def deploy(self, ip: str, title: str, content: str, color: str) -> None:
        """ 消息卡片：'部署'模板 """
        color = ColorStyle.red.value if color.lower() == 'red' else ColorStyle.blue.value

        self.card = {
            "config": {
                "wide_screen_mode": True
            },
            "elements": [
                {
                    "fields": [
                        {
                            "is_short": True,
                            "text": {
                                "content": "**时间**  {now}\n".format(now=datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                                "tag": "lark_md"
                            }
                        },
                        {
                            "is_short": True,
                            "text": {
                                "content": "**IP 地址**  {ip}\n".format(ip=ip),
                                "tag": "lark_md"
                            }
                        }
                    ],
                    "tag": "div"
                },
                {
                    "tag": "div",
                    "text": {
                        "content": "{desc}\n".format(desc=content),
                        "tag": "lark_md"
                    }
                },
                {
                    "tag": "hr"
                },
                {
                    "elements": [
                        {
                            "content": "[来自变更通知](https://www.open.feishu.cn/)",
                            "tag": "lark_md"
                        }
                    ],
                    "tag": "note"
                }
            ],
            "header": {
                "template": f"{color}",
                "title": {
                    "content": f"{title}",
                    "tag": "plain_text"
                }
            }
        }
