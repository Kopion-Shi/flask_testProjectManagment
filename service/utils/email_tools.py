#!/usr/bin/python
# -*- coding: UTF-8 -*-
import yagmail
import traceback
from config import config

'''
receivers 收件人，字符数组['邮件地址']
subject 邮件主题, 字符串
contents 邮件内容，自定义 字符数组
attachments 附件默认为空
'''


def sendEmail(receivers, subject, contents, attachments=[]):
    try:
        # 初始化服务对象直接根据参数给定，更多参考SMTP(）内部
        server = yagmail.SMTP(host=config.EMAIL_HOST, port=config.EMAIL_PORT,
                              user=config.EMAIL_HOST_USER, password=config.EMAIL_HOST_PASSWORD)
        # 发送内容，设置接受人等信息，更多参考SMTP.send()内部
        server.send(to=receivers,
                    subject=subject,
                    contents=contents,
                    attachments=attachments)
        server.close()
    except Exception:
        print('traceback.format_exc(): {}'.format(traceback.format_exc()))
        return False

    # 无任何异常表示发送成功
    return True


if __name__ == "__main__":
    # 测试发送服务
    receivers = ['Carl3633524461@outlook.com',]
    subject = 'tool email send test'
    body = 'hello word'
    sendEmail(receivers, subject, [body])
