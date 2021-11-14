# -*- coding: utf-8 -*-
# @Time    : 2021/11/7 11:37 下午 
# @Author  : xujunpeng
import copy
import functools
import inspect
from app import app
from flask import g
from py_zipkin.zipkin import zipkin_span, create_attrs_for_span
from py_zipkin.transport import SimpleHTTPTransport
from py_zipkin.encoding import Encoding
from py_zipkin.util import generate_random_64bit_string, ZipkinAttrs
from six.moves.urllib.request import Request
from six.moves.urllib.request import urlopen


class TraceDecorator(type):
    def __new__(cls, cls_name, bases, dic):
        for name, value in dic.items():
            # TODO 原来的函数就不能有装饰器了, 这个做法就是为了消除类下的函数有装饰器
            if hasattr(value, "__qualname__") and cls_name in value.__qualname__ and inspect.isroutine(value):
                dic[name] = Trace(value)
        return super().__new__(cls, cls_name, bases, dic)


class Trace:

    def __init__(self, func):
        self.func = func
        self.attr = None

    def __call__(self, *args, **kwargs):
        # 如果获取不到，那说明 before_request出现异常
        ctx = getattr(g, app.config["ZIPKIN_TRACE"], Exception("TRACE INFO MISSING"))
        if ctx:
            self.attr = ZipkinAttrs(
                span_id=generate_random_64bit_string(),
                trace_id=ctx.trace_id,
                flags=ctx.flags,
                parent_span_id=ctx.parent_span_id,
                is_sampled=ctx.is_sampled,
            )
        else:
            self.attr = create_attrs_for_span()
        span_name = self.func.__module__ + "-" + self.func.__name__
        # TODO 使用kafka
        with zipkin_span(
                service_name="MyFlask", span_name=span_name, sample_rate=app.config["ZIPKIN_SAMPLE_RATE"],
                transport_handler=HTTPTransport(app.config["ZIPKIN_HOST"], app.config["ZIPKIN_PORT"]),
                encoding=Encoding.V2_JSON,
                zipkin_attrs=self.attr
        ) as span:
            setattr(g, app.config["ZIPKIN_TRACE"], self.attr)
            span.update_binary_annotations({"update_binary_annotations": "fortest"})
            return self.func(*args, **kwargs)

    def __get__(self, instance, instancetype):
        """Implement the descriptor protocol to make decorating instance
        method possible.
        """
        # Return a partial function with the first argument is the instance
        #   of the class decorated.
        if instance:
            return functools.partial(self.__call__, instance)
        return functools.partial(self.__call__)


class HTTPTransport(SimpleHTTPTransport):

    def send(self, payload):
        path, content_type = self._get_path_content_type(payload)
        url = "http://{}:{}{}".format(self.address, self.port, path)

        req = Request(url, payload.encode(), {"Content-Type": content_type})
        response = urlopen(req)

        assert response.getcode() == 202
