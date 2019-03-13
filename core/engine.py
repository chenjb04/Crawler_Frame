# -*- coding:utf-8 -*-
__author__ = 'ChenJiaBao'
__date__ = '2019/3/13 17:00'
# 引擎
from .downloader import Downloader
from .spider import Spider
from .scheduler import Scheduler
from .pipeline import Pipeline
from http.request import Request


class Engine(object):
    """
    提供程序入口，调用其他组件，实现整个框架的运作
    """
    def __init__(self):
        """
        初始化各个组件
        """
        self.scheduler = Scheduler()
        self.downloader = Downloader()
        self.pipeline = Pipeline()
        self.spider = Spider()

    def start(self):
        """
        启动引擎
        :return:
        """
        self._start_engine()

    def _start_engine(self):
        """
        具体实现引擎
        :return:
        """
        # 调用spider start_request方法，获取request对象
        start_request = self.spider.start_requests()
        # 调用scheduler add_request方法，添加到调度器
        self.scheduler.add_request(start_request)
        # 调用scheduler get_request方法，获取request对象
        request = self.scheduler.get_request()
        # 调用下载器的get_response方法，获取响应
        response = self.downloader.get_response(request)
        # 调用爬虫的parse方法， 处理响应
        result = self.spider.parse(response)
        # 判断结果，如果为request对象，重新调用调度器的add_request方法
        if isinstance(result, Request):
            self.scheduler.add_request(result)
        # 如果不是，调用pipeline的Process_item方法,处理结果
        else:
            self.pipeline.process_item(result)
