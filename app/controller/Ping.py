# -*- coding: utf-8 -*-
# @Time    : 2021/10/24 3:33 下午 
# @Author  : xujunpeng
from typing import List, Dict
from app.base.base_controller import BaseController


class PingController(BaseController):

    def get(self, *args, **kwargs):
        pass

    def create(self, *args, **kwargs):
        pass

    def query(self, page=1, offset=10, sort: List[set] = None, query: Dict = None):
        pass
