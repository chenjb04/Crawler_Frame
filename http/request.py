# -*- coding:utf-8 -*-
__author__ = 'ChenJiaBao'
__date__ = '2019/3/13 17:01'
# Request对象


class Request(object):
    """
    框架内置请求对象
    """

    def __init__(self, url, method='GET', headers=None, params=None, data=None):
        """
        初始化request对象
        :param url: 请求地址
        :param method: 请求方法
        :param headers: 请求头
        :param params: 请求参数
        :param data: 请求体
        """
        self.url = url
        self.method = method
        self.headers = headers
        self.params = params
        self.data = data
