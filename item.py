# -*- coding:utf-8 -*-
__author__ = 'ChenJiaBao'
__date__ = '2019/3/13 17:02'
# item对象


class Item(object):
    """
    框架内置Item对象
    """
    def __init__(self, data):
        """
        初始化item对象
        :param data: 传入的数据
        """
        self._data = data

    @property
    def data(self):
        """
        使data只读,保护data
        :return:
        """
        return self._data
