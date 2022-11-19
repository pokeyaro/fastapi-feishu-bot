# -*- coding: utf-8 -*-
import uuid

from feishu.lark.card import TemplateCard
from feishu.utils.wrapper import LarkRequest


def send_message(email: str, **kwargs) -> (dict, object):

    """
    服务端文档 -> 消息与群组 -> 消息 -> 发送消息
    https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/message/create
    """

    # Api资源路径
    api = '/open-apis/im/v1/messages'

    # 请求方式
    method = 'POST'

    # 设置请求参数
    query = {
        'receive_id_type': 'email',
    }

    # 设置请求体
    msg_type = 'interactive'
    card = TemplateCard()
    card.deploy(ip=kwargs['ip'], title=kwargs['title'], content=kwargs['content'], color=kwargs['color'])
    content = card.to_json
    unique_code = str(uuid.uuid4())
    data = {
        'receive_id': email,      # [必填] 依据receive_id_type的值，填写对应的消息接收者id
        'msg_type': msg_type,     # [必填] 消息类型
        'content': content,       # [必填] 消息内容，json结构序列化后的字符串
        'uuid': unique_code       # [非必填] 用于发送消息请求去重, 持有相同uuid的请求1小时内至多成功执行一次
    }

    resp, r = LarkRequest(
        api=api,
        method=method,
        headers=None,
        params=query,
        payload=data,
    ).send

    return resp, r


if __name__ == '__main__':
    user = "xiaoming@gmail.com"
    d = {
        "ip": "10.80.110.1",
        "title": "【通知】部署 - 关键节点通知",
        "content": "上线检查：\n1. user check pass\n2. ssh check pass\n3. pub key check pass\n～",
        "color": "blue",
    }
    send_message(user, **d)
