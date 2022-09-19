from celery import shared_task
from .dingtalk import send

@shared_task
def send_dingtalkmessage(message):
    send(message)