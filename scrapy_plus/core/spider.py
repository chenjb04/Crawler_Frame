# -*- coding:utf-8 -*-
__author__ = 'ChenJiaBao'
__date__ = '2019/3/13 17:01'
# spider组件
from scrapy_plus.http.request import Request
from scrapy_plus.item import Item


class Spider(object):
    """
    spider对象封装
    """
    start_url = 'http://www.baidu.com'

    def start_requests(self):
        """
        构造start_url地址的请求
        :return:
        """
        return Request(self.start_url)

    def parse(self, response):
        """
        处理start_url请求的响应
        :param response: response对象
        :return:
        """
        return Item(response.body)


