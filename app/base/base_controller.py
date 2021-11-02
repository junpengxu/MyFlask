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
        result = []

        # 添加这个创建时间的过滤是为了兼容处理后台创建的数据展示，展示当前时间点之前的数据
        _q = and_(Ugc.is_online == True, Ugc.create_time <= datetime.datetime.now())
        if content:
            _q = and_(_q, or_(Ugc.content.like('%' + content + '%'), Ugc.title.like('%' + content + '%')))
        for k, v in filter.items():
            # 如果v不为空，这里是包括了 "", None
            if hasattr(Ugc, k) and v:
                _q = and_(_q, getattr(Ugc, k) == v)

        # query的实现可以参考es的做法

        query = {
            ""
        }

        _query = {}

        # 默认id降序
        _sort = [self.model.id.desc()]
        for k, v in sort:
            if v:
                # 为true则代表降序
                _sort.append(getattr(self.model, k).desc())
            else:
                _sort.append(getattr(self.model, k).asc())

        # 如果要查询两次， 目前比较容易的方式就是查询两次
        # total_nums = self.model.query.filter().order_by(*_sort).count()
        objs = self.model.query.filter().order_by(*_sort).paginate(
            page=page, per_page=offset, error_out=False
        ).items
        for obj in objs:
            result.append(obj.get_detail())
        # 如果需要返回总数， 则要查询遍
        return {"result": result}

    def offline(self, pk):
        pass

    def get_by_ids(self, ids=None):
        if ids is None:
            ids = []
