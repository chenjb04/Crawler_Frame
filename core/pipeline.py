# -*- coding:utf-8 -*-
__author__ = 'ChenJiaBao'
__date__ = '2019/3/13 17:01'
# 管道


class Pipeline(object):
    """
    管道对象封装
    """

    def process_item(self, item):
        """
        处理item
        :param item: item对象
        :return:
        """
        print("item:", item)