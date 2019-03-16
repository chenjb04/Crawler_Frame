# -*- coding:utf-8 -*-
__author__ = 'ChenJiaBao'
__date__ = '2019/3/16 18:45'
import redis
from scrapy_plus.conf.settings import REDIS_QUEUE_NAME, REDIS_QUEUE_HOST, REDIS_QUEUE_PORT, REDIS_QUEUE_DB


# redis队列默认配置
# REDIS_QUEUE_NAME = 'request_queue'
# REDIS_QUEUE_HOST = 'localhost'
# REDIS_QUEUE_PORT = 6379
# REDIS_QUEUE_DB = 10


class StatsCollector(object):

    def __init__(
            self,
            spider_names=[],
            host=REDIS_QUEUE_HOST,
            port=REDIS_QUEUE_PORT,
            db=REDIS_QUEUE_DB,
            password=None):

        self.redis = redis.StrictRedis(
            host=host, port=port, db=db, password=password)
        # 存储请求数量的键
        self.request_num_key = "_".join(spider_names) + "_request_num"
        # 存储响应数量的键
        self.response_num_key = "_".join(spider_names) + "_response_num"
        # 存储重复请求的键
        self.repeat_request_num_key = "_".join(
            spider_names) + "_repeat_request_num"
        # 存储start_request数量的键
        self.start_request_num_key = "_".join(
            spider_names) + "_start_request_num"

    def incr(self, key):
        """给键对应的值增加1，不存在会自动创建，并且值为1，"""
        self.redis.incr(key)

    def get(self, key):
        """获取键对应的值，不存在是为0，存在则获取并转化为int类型"""
        ret = self.redis.get(key)
        if not ret:
            ret = 0
        else:
            ret = int(ret)
        return ret

    def clear(self):
        """程序结束后清空所有的值"""
        self.redis.delete(
            self.request_num_key,
            self.response_num_key,
            self.repeat_request_num_key,
            self.start_request_num_key)

    @property
    def request_num(self):
        """获取请求数量"""
        return self.get(self.request_num_key)

    @property
    def response_num(self):
        """获取响应数量"""
        return self.get(self.response_num_key)

    @property
    def repeat_request_num(self):
        """获取重复请求数量"""
        return self.get(self.repeat_request_num_key)

    @property
    def start_request_num(self):
        """获取start_request数量"""
        return self.get(self.start_request_num_key)
