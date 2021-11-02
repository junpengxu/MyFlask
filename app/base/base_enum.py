# -*- coding: utf-8 -*-
# @Time    : 2021/10/24 1:16 下午 
# @Author  : xujunpeng
from enum import Enum


class BaseEnum(Enum):

    @property
    def code(self):
        return self.value

    @code.getter
    def code(self):
        return self.value[0]

    @property
    def desc(self):
        return self.value

    @desc.getter
    def desc(self):
        return self.value[1]
