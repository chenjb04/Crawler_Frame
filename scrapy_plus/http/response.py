# -*- coding:utf-8 -*-
__author__ = 'ChenJiaBao'
__date__ = '2019/3/13 17:02'
# Response对象
from lxml import etree
import json
import re


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

    def xpath(self, rule):
        """
        添加xpath方法
        :param rule: xpath提取规则
        :return:
        """
        html = etree.HTML(self.body)
        return html.xpath(rule)

    @property
    def json(self):
        """
        添加json方法
        :return:
        """
        return json.loads(self.body.decode())

    def re_findall(self, rule):
        """
        添加正则findall方法
        :param rule: 正则提取规则
        :return:
        """
        return re.findall(rule, self.body.decode())