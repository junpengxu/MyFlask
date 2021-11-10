# -*- coding: utf-8 -*-
# @Time    : 2021/11/7 11:37 下午 
# @Author  : xujunpeng
import copy

from py_zipkin.zipkin import zipkin_span, create_attrs_for_span
from py_zipkin.transport import SimpleHTTPTransport
from py_zipkin.encoding import Encoding
from py_zipkin.util import generate_random_64bit_string, ZipkinAttrs

from werkzeug.local import LocalStack, LocalProxy

_ctx_stack = LocalStack()


class Trace:

    def get_current_ctx(self):
        # do something to get User object and return it
        return _ctx_stack.pop()

    def __init__(self, func):
        self.func = func
        self.attr = None
        self._attr = create_attrs_for_span()
        self.current_ctx = LocalProxy(self.get_current_ctx)

    def __call__(self, *args, **kwargs):
        ctx = copy.deepcopy(self.current_ctx)  # 执行完这一行，栈已经被pop出
        if ctx:
            self.attr = ZipkinAttrs(
                span_id=generate_random_64bit_string(),
                trace_id=ctx["trace_id"],
                flags=ctx["flags"],
                parent_span_id=ctx["span_id"],
                is_sampled=ctx["is_sampled"]
            )
        else:
            self.attr = self._attr
        with zipkin_span(
                service_name="myflask", span_name=self.func.__module__, sample_rate=100,
                transport_handler=SimpleHTTPTransport('242.193.113.198', 9411),
                encoding=Encoding.V1_THRIFT,
                zipkin_attrs=self.attr
        ):
            _ctx_stack.push({
                "trace_id": self.attr.trace_id,
                "span_id": self.attr.span_id,
                "is_sampled": self.attr.is_sampled,
                "flags": self.attr.flags,
            })
            return self.func(*args, **kwargs)

# def trace(func):
#     @zipkin_span(service_name="myflask", span_name=func.__module__, sample_rate=100,
#                  transport_handler=SimpleHTTPTransport('42.193.113.198', 9411), encoding=Encoding.V1_THRIFT)
#     def wrap(*args, **kwargs):
#         return func(*args, **kwargs)
#
#     return wrap
