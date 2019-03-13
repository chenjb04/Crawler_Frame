# -*- coding:utf-8 -*-
__author__ = 'ChenJiaBao'
__date__ = '2019/3/13 17:00'
# 引擎
from .downloader import Downloader
from .spider import Spider
from .scheduler import Scheduler
from .pipeline import Pipeline
from scrapy_plus.http.request import Request
from scrapy_plus.middlewares.spider_middlewares import SpiderMiddleware
from scrapy_plus.middlewares.downloader_middlewares import DownloaderMiddleware


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
        self.spider_middleware = SpiderMiddleware()
        self.downloader_middleware = DownloaderMiddleware()

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
        # 对start_request处理
        start_request = self.spider_middleware.process_request(start_request)
        # 调用scheduler add_request方法，添加到调度器
        self.scheduler.add_request(start_request)
        # 调用scheduler get_request方法，获取request对象
        request = self.scheduler.get_request()
        # request对象经过下载器中间件处理
        request = self.downloader_middleware.process_request(request)
        # 调用下载器的get_response方法，获取响应
        response = self.downloader.get_response(request)
        # response经过下载器中间件和爬虫中间件处理
        response = self.downloader_middleware.process_response(response)
        response = self.spider_middleware.process_response(response)
        # 调用爬虫的parse方法， 处理响应
        result = self.spider.parse(response)
        # 判断结果，如果为request对象，重新调用调度器的add_request方法
        if isinstance(result, Request):
            result = self.spider_middleware.process_request(result)
            self.scheduler.add_request(result)
        # 如果不是，调用pipeline的process_item方法,处理结果
        else:
            self.pipeline.process_item(result)
