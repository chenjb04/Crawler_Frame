# -*- coding:utf-8 -*-
__author__ = 'ChenJiaBao'
__date__ = '2019/3/13 17:01'
# 下载器
import requests

from scrapy_plus.http.response import Response
from scrapy_plus.utils.log import logger


class Downloader(object):
    """
    下载器：根据请求对象发送http或https请求，获取响应
    """
    def get_response(self, request):
        """
        获取请求返回的响应
        :param request:
        :return:
        """
        if request.method.upper() == 'GET':
            resp = requests.get(request.url, headers=request.headers, params=request.params)
        elif request.method.upper() == 'POST':
            resp = requests.get(request.url, headers=request.headers, params=request.params, data=request.data)
        else:
            raise Exception("不支持的请求方法：<{}>".format(request.method))
        logger.info("<{} {}>".format(resp.status_code, resp.request.url))
        return Response(url=resp.url, body=resp.content, headers=resp.headers, status_code=resp.status_code)
