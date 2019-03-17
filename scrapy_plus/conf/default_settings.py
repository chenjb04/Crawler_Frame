# -*- coding:utf-8 -*-
__author__ = 'ChenJiaBao'
__date__ = '2019/3/13 20:21'
import logging


# 默认的配置
DEFAULT_LOG_LEVEL = logging.INFO    # 默认等级
DEFAULT_LOG_FMT = '%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s: %(message)s'   # 默认日志格式
DEFUALT_LOG_DATEFMT = '%Y-%m-%d %H:%M:%S'  # 默认时间格式
DEFAULT_LOG_FILENAME = 'log.log'    # 默认日志文件名称

# 设置并发数量
CONCURRENT_REQUEST = 5

# 异步方式
ASYNC_TYPE = 'coroutine'

# 分布式
SCHEDULER_PERSIST = True

# redis队列默认配置
REDIS_QUEUE_NAME = 'request_queue'
REDIS_QUEUE_HOST = 'localhost'
REDIS_QUEUE_PORT = 6379
REDIS_QUEUE_DB = 0

# redis指纹集合
REDIS_SET_NAME = "redis_set"
REDIS_SET_HOST = "localhost"
REDIS_SET_PORT = 6379
REDIS_SET_DB = 0

#redi备份的位置
REDIS_BACKUP_NAME = "redis_backup"
REDIS_BACKUP_HOST = "localhost"
REDIS_BACKUP_PORT = 6379
REDIS_BACKUP_DB = 0

MAX_RETRY_TIME = 3