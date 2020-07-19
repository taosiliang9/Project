"""
author: taosiliang
create: time: 2020-07-09
update：time: 2020-07-11
"""




from login.models import EmailVerifyRecord
from random import Random
from mysite_login.settings import EMAIL_FROM
from django.core.mail import send_mail
import string
import random


def random_str(randomlength=8):
    str = ''
    chars = 'abcdefghijklmnopqrstuvwsyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


# 发送注册邮件
def send_register_email(request_uri, email, send_type='register'):
    # 发送之前先保存到数据库，到时候查询链接是否存在

    # 实例化一个EmailVerifyRecord对象
    email_record = EmailVerifyRecord()
    # 生成随机的code放入链接
    code = random_str(16)

    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type

    email_record.save()

    # 定义邮件内容
    email_title = ''
    email_body = ''

    if send_type == 'register':
        email_title = '注册激活链接'
        email_body = '请点击链接激活账号：{}active/{}'.format(request_uri, code)  # request_uri='http://127.0.0.1:8000/register/'

        # 使用Django内置函数完成邮件发送。四个参数：主题，邮件内容，从哪里发，接受者list
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            return True
        else:
            return False

    elif send_type == 'forget':
        email_title = '密码重置链接'
        email_body = '请点击链接重置密码：{}reset/{}'.format(request_uri, code)  # request_uri='http://127.0.0.1:8000/forgetpwd/'

        # 使用Django内置函数完成邮件发送。四个参数：主题，邮件内容，从哪里发，接受者list
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            return True
        else:
            return False
