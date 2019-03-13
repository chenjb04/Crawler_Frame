# -*- coding:utf-8 -*-
__author__ = 'ChenJiaBao'
__date__ = '2019/3/13 17:00'
# 调度器封装
from queue import Queue


class Scheduler(object):
    """
    scheduler:缓存请求对象，为下载器提供请求对象，对请求对象进行去重
    """
    def __init__(self):
        self.queue = Queue()

    def add_request(self, request):
        """
        添加request到队列
        :param request: 请求对象
        :return:
        """
        self.queue.put(request)

    def get_request(self):
        """
        从队列中取request对象
        :return:
        """
        try:
            return self.queue.get(block=False)
        except:
            return None

    def _filter_request(self, request):
        """
        对request进行去重
        :param request:请求对象
        :return:
        """
        pass