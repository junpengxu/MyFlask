# -*- coding: utf-8 -*-
# @Time    : 2021/10/24 1:16 下午 
# @Author  : xujunpeng
from typing import List, Dict


class BaseController:

    def __init__(self, model):
        self.model = model

    def get(self, pk):
        obj = self.model.query.get(pk)
        if not obj:
            return {}
        else:
            return obj.get_detail()

    def create(self, *args, **kwargs):
        pass

    def query(self, page=1, offset=10, sort: List[set] = None, query: Dict = None):
        """
        :param page: 起始页面
        :param offset: 每页查询数量
        :param content: 查找条件， 用来固定一个查询的字段与业务做绑定，
                e.g _q = Model.name.like('%' + content + '%')
        :param query: 匹配条件, 目前只支持等于的判断。
        :param sort: 排序条件,
        :return:
        """

        offset = 20 if offset > 20 else offset
        return {"result": []}

    def offline(self, pk):
        pass

    def get_by_ids(self, ids=None):
        if ids is None:
            ids = []
