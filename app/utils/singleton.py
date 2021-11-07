# -*- coding: utf-8 -*-
# @Time    : 2021/11/3 11:20 下午
# @Author  : xujunpeng


def singleton(cls):
    instances = {}

    def getinstance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return getinstance
