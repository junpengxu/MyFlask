# -*- coding: utf-8 -*-
# @Time    : 2021/11/7 11:37 下午 
# @Author  : xujunpeng
import copy
import functools
import inspect

from app import ctx_stack

from py_zipkin.zipkin import zipkin_span, create_attrs_for_span
from py_zipkin.transport import SimpleHTTPTransport
from py_zipkin.encoding import Encoding
from py_zipkin.util import generate_random_64bit_string, ZipkinAttrs
from werkzeug.local import LocalProxy
from six.moves.urllib.request import Request
from six.moves.urllib.request import urlopen


class TraceDecorator(type):
    def __new__(cls, cls_name, bases, dct):
        for name, value in dct.items():
            if inspect.isroutine(value):
                # TODO 原来的函数就不能有装饰器了
                dct[name] = Trace(value)
        return super().__new__(cls, cls_name, bases, dct)


class Trace:

    def __init__(self, func):
        self.func = func
        self.attr = None

    def __call__(self, *args, **kwargs):
        ctx = copy.deepcopy(LocalProxy(lambda: ctx_stack.pop()))  # 执行完这一行，栈已经被pop出
        if ctx:
            self.attr = ZipkinAttrs(
                span_id=generate_random_64bit_string(),
                trace_id=ctx["trace_id"],
                flags=ctx["flags"],
                parent_span_id=ctx["span_id"],
                is_sampled=ctx["is_sampled"]
            )
        else:
            self.attr = create_attrs_for_span()
        span_name = self.func.__module__ + "-" + self.func.__name__
        with zipkin_span(
                service_name="xdd-dcd", span_name=span_name, sample_rate=100,
                transport_handler=HTTPTransport('42.193.113.198', 9411),
                encoding=Encoding.V2_JSON,
                zipkin_attrs=self.attr
        ):
            ctx_stack.push({
                "trace_id": self.attr.trace_id,
                "span_id": self.attr.span_id,
                "is_sampled": self.attr.is_sampled,
                "flags": self.attr.flags,
            })
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
