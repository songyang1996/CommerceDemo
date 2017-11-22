from django.conf import settings
from django.core.mail import send_mail
from celery import Celery

# 导入django所需的环境变量 以下四行在celery服务器才需要添加
# import os
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dailyfresh.settings")
# import django
# django.setup()

app = Celery("celery_tasks.task", broker="redis://192.168.64.99/6379/10")

@app.task
def send_active_email(toemail, username, token):
    '''向用户发送激活文件'''
    sender = settings.EMAIL_FROM
    receiver = [toemail]
    html_message = '<h1>欢迎%s来到天天生鲜网站</h1>请点击下面的链接进行激活<a href="http://127.0.0.1:8000/user/active/%s/">http://127.0.0.1:8000/user/active/%s/</a>'%(username, token, token)
    send_mail("用户激活测试", '', sender, receiver, html_message=html_message)
    # send_mail参数 title message sender receiver, html_message(可选)
