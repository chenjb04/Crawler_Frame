# -*- coding:utf-8 -*-
__author__ = 'ChenJiaBao'
__date__ = '2019/3/13 17:01'
# Request对象


class Request(object):
    """
    框架内置请求对象
    """

    def __init__(self, url, method='GET', headers=None, params=None, data=None, parse='parse', meta=None, filter=True):
        """
        初始化request对象
        :param url: 请求地址
        :param method: 请求方法
        :param headers: 请求头
        :param params: 请求参数
        :param data: 请求体
        :param parse: 解析函数的函数名
        :param meta: 不同解析函数之间传递数据
        :param filter: 请求是否去重
        """
        self.url = url
        self.method = method
        self.headers = headers
        self.params = params
        self.data = data
        self.parse = parse
        self.meta = meta
        # 默认为去重，False不进行去重
        self.filter = filter
        # 重试次数
        self.retry_time = 0