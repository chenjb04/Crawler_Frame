# -*- coding:utf-8 -*-
__author__ = 'ChenJiaBao'
__date__ = '2019/3/13 19:02'
# 下载中间件


class DownloaderMiddleware(object):
    """
    下载中间件封装
    """
    def process_request(self, request):
        """
        对request处理
        :param request:request对象
        :return:
        """
        # print("下载器中间件：process_request")
        return request

    def process_response(self, response):
        """
        对response处理
        :param response:响应对象
        :return:
        """
        # print('下载器中间件：process_response')
        return response
