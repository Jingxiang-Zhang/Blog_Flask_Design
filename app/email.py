from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from . import mail


def send_async_email(app, msg):
    """
    改进方法，可以使用消息队列进行发送，当多个邮件进行发送的时候开启多个线程
    :param app:
    :param msg:
    :return:
    """
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    """
    发送邮件
    改进方法，不从config中接收主题之类的参数，因为每次的邮件内容可能不同
    :param to: 邮件接受者
    :param subject:
    :param template: 选用的email模板
    :param kwargs:
    :return:
    """
    app = current_app._get_current_object()
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr
