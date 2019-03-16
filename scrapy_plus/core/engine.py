# -*- coding:utf-8 -*-
__author__ = 'ChenJiaBao'
__date__ = '2019/3/13 17:00'
# 引擎
from datetime import datetime
import importlib

from .downloader import Downloader
from .scheduler import Scheduler
from scrapy_plus.http.request import Request
from scrapy_plus.utils.log import logger
from scrapy_plus.conf.settings import SPIDERS, PIPELINES, SPIDER_MIDDLEWARES, DOWNLOADER_MIDDLEWARES


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
        self.pipelines = self._auto_import_instances(PIPELINES)
        self.spiders = self._auto_import_instances(SPIDERS, is_spider=True)
        self.spider_middlewares = self._auto_import_instances(SPIDER_MIDDLEWARES)
        self.downloader_middlewares = self._auto_import_instances(DOWNLOADER_MIDDLEWARES)
        self.total_request_num = 0
        self.total_response_num = 0

    def _auto_import_instances(self, path, is_spider=False):
        """
        实现模块动态导入。传入模块路径列表
        :param path:
        :return:
        """
        if is_spider:
            instances = {}
        else:
            instances = []
        for p in path:
            # 模块路径名称
            module_name = p.rsplit(".", 1)[0]
            # 类名
            cls_name = p.rsplit(".", 1)[-1]
            module = importlib.import_module(module_name)
            # 获取module下的类
            cls = getattr(module, cls_name)
            if is_spider:
                instances[cls().name] = cls()
            else:
                instances.append(cls())
        return instances

    def start(self):
        """
        启动引擎
        :return:
        """
        start_time = datetime.now()
        logger.info('爬虫启动：{}'.format(start_time))
        logger.info('当前启动的爬虫：{}'.format(SPIDERS))
        logger.info("当前开启的管道：{}".format(PIPELINES))
        logger.info("当前开启爬虫的中间件：{}".format(SPIDER_MIDDLEWARES))
        logger.info("当前开启下载器的中间件：{}".format(DOWNLOADER_MIDDLEWARES))
        self._start_engine()
        end_time = datetime.now()
        logger.info('爬虫结束：{}'.format(end_time))
        logger.info('爬虫共运行：{}秒'.format((end_time-start_time).total_seconds()))
        logger.info('总的请求数量：{}个'.format(self.total_request_num))
        logger.info('总的响应数量：{}个'.format(self.total_response_num))
        logger.info('总的重复数量：{}个'.format(self.scheduler.repeat_request_num))

    def _start_request(self):
        """
        初始化请求，调用spider的start_request方法，所有请求添加到调度器
        :return:
        """
        for spider_name, spider in self.spiders.items():
            # 调用spider start_request方法，获取request对象
            for start_request in spider.start_requests():
                # 对start_request处理
                for spider_middleware in self.spider_middlewares:
                    start_request = spider_middleware.process_request(start_request)
                # 初始请求添加spider_name
                start_request.spider_name = spider_name
                # 调用scheduler add_request方法，添加到调度器
                self.scheduler.add_request(start_request)
                self.total_request_num += 1

    def _execute_request_response_item(self):
        """
        处理单个请求，从调度器取出，发送请求，获取响应，处理请求
        :return:
        """
        # 调用scheduler get_request方法，获取request对象
        request = self.scheduler.get_request()
        if request is None:
            return
        # request对象经过下载器中间件处理
        for downloader_middleware in self.downloader_middlewares:
            request = downloader_middleware.process_request(request)
        # 调用下载器的get_response方法，获取响应
        response = self.downloader.get_response(request)
        # request meta值传递给response meta
        response.meta = request.meta
        # response经过下载器中间件和爬虫中间件处理
        for downloader_middleware in self.downloader_middlewares:
            response = downloader_middleware.process_response(response)
        for spider_middleware in self.spider_middlewares:
            response = spider_middleware.process_response(response)
        # 获取request对象响应的parse方法
        spider = self.spiders[request.spider_name]
        parse = getattr(spider, request.parse)
        # 调用爬虫的parse方法， 处理响应
        for result in parse(response):
            # 判断结果，如果为request对象，重新调用调度器的add_request方法
            if isinstance(result, Request):
                for spider_middleware in self.spider_middlewares:
                    result = spider_middleware.process_request(result)
                result.spider_name = request.spider_name
                self.scheduler.add_request(result)
                self.total_request_num += 1
            # 如果不是，调用pipeline的process_item方法,处理结果
            else:
                # 变量所有的管道
                for pipeline in self.pipelines:
                    result = pipeline.process_item(result, spider)
        self.total_response_num += 1

    def _start_engine(self):
        """
        具体实现引擎
        :return:
        """
        self._start_request()
        while True:
            self._execute_request_response_item()
            if self.total_response_num + self.scheduler.repeat_request_num >= self.total_request_num:
                break

