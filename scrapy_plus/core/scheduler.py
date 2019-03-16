# -*- coding:utf-8 -*-
__author__ = 'ChenJiaBao'
__date__ = '2019/3/13 17:00'
# 调度器封装
from queue import Queue
import w3lib.url
from hashlib import sha1

from scrapy_plus.utils.log import logger
from scrapy_plus.utils.redis_queue import Queue as RedisQueue
from scrapy_plus.conf.settings import SCHEDULER_PERSIST
from scrapy_plus.utils.set import NoramlFilterContainer, RedisFilterContainer


class Scheduler(object):
    """
    scheduler:缓存请求对象，为下载器提供请求对象，对请求对象进行去重
    """
    def __init__(self, collector):
        if not SCHEDULER_PERSIST:
            self.queue = Queue()
            # 保存指纹的集合
            self._filter_container = NoramlFilterContainer()
        else:
            # 分布式 redisqueue
            self.queue = RedisQueue()
            # 保存分布式指纹的集合
            self._filter_container = RedisFilterContainer()
        # 重复的数量
        # self.repeat_request_num = 0
        self.collector = collector

    def add_request(self, request):
        """
        添加request到队列
        :param request: 请求对象
        :return:
        """
        if self._filter_request(request):
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
        # request对象添加fp属性，保存指纹
        request.fp = self._gen_fp(request)
        if not self._filter_container.exists(request.fp):
            self._filter_container.add_fp(request.fp)
            return True
        else:
            logger.info("发现重复请求：<{} {}>".format(request.method, request.url))
            self.collector.incr(self.collector.repeat_request_num_key)

    def _gen_fp(self, request):
        """
        生成request对象指纹
        :param request:
        :return:
        """
        # 对url地址进行排序
        url = w3lib.url.canonicalize_url(request.url)
        # 请求方法
        method = request.method.upper()
        # 请求参数
        params = request.params if request.params is not None else {}
        params = str(sorted(params.items(), key=lambda x: x[0]))
        # 请求体
        data = request.data if request.data is not None else {}
        data = str(sorted(data.items(), key=lambda x: x[0]))
        # 使用sha1加密
        fp = sha1()
        fp.update(self._to_bytes(url))
        fp.update(self._to_bytes(method))
        fp.update(self._to_bytes(params))
        fp.update(self._to_bytes(data))

        return fp.hexdigest()

    @staticmethod
    def _to_bytes(string):
        """
        将字符串转换为bytes
        :param string:
        :return:
        """
        return string.encode("utf-8")