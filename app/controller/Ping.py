# -*- coding: utf-8 -*-
# @Time    : 2021/10/24 3:33 下午 
# @Author  : xujunpeng
import time
from typing import List, Dict
from app.base.base_controller import BaseController
from app.model.Ping import Ping


class PingController(BaseController):

    def get(self, pk):
        Ping.query.get(pk).simple_info()
        Ping.query.filter().all()
        return Ping.query.get(pk).simple_info()

    def create(self, *args, **kwargs):
        desc = kwargs.get("desc", "default")
        Ping(desc=desc).save()

    def query(self, page=1, offset=10, sort: List[set] = None, query: Dict = None):
        pass
