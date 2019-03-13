# -*- coding:utf-8 -*-
__author__ = 'ChenJiaBao'
__date__ = '2019/3/13 17:02'
# Response对象


class Response(object):
    """
    框架内置Response对象
    """
    def __init__(self, url, status_code, headers, body):
        """
        初始化response对象
        :param url: 响应url地址
        :param status_code: 响应状态码
        :param headers: 响应头
        :param body: 响应体
        """
        self.url = url
        self.status_code = status_code
        self.headers = headers
        self.body = body
