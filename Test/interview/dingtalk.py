# coding=utf-8
### 通知
from typing import Text
from dingtalkchatbot.chatbot import DingtalkChatbot

from django.conf import settings

def send(message, at_mobiles=[]):
    webhook = settings.DINGTALK_WEB_HOOK
    
    # 初始化机器人
    DingDing = DingtalkChatbot(webhook)

    #Text消息所有人
    DingDing.send_text(msg=('面试通知: %s' % message), at_mobiles = at_mobiles)