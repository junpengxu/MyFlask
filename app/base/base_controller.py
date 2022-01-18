# -*- coding: utf-8 -*-
# @Time    : 2021/10/24 1:16 下午 
# @Author  : xujunpeng
import inspect

from app.utils.trace import TraceDecorator


class ControllerTrace(metaclass=TraceDecorator):

    def get(self, *args, **kwargs):
        pass

    def create(self, *args, **kwargs):
        pass

    def query(self, *args, **kwargs):
        pass


class BaseController(ControllerTrace):
    pass
