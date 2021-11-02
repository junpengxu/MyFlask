# -*- coding: utf-8 -*-
# @Time    : 2021/10/24 3:33 下午 
# @Author  : xujunpeng
from typing import List, Dict

from app.base.base_controller import BaseController


class PingController(BaseController):
    def __init__(self, model):
        super().__init__(model)

    def get(self, pk):
        return super().get(pk)

    def create(self, *args, **kwargs):
        super().create(*args, **kwargs)

    def query(self, page=1, offset=10, sort: List[set] = None, query: Dict = None):
        return super().query(page, offset, sort, query)

    def offline(self, pk):
        super().offline(pk)

    def get_by_ids(self, ids=None):
        super().get_by_ids(ids)
