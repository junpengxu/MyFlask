# -*- coding: utf-8 -*-
# @Time    : 2021/10/31 2:44 下午 
# @Author  : xujunpeng

from redlock import Redlock, MultipleRedlockException
from app import app


class RedLock:
    def __init__(self, key, timeout=300):
        self.lock = None
        self.key = key
        self.timeout = timeout
        self.dlm = Redlock(connection_list=app.config["RED_LOCK_CONFIG"], retry_count=3, retry_delay=100)

    def __lock(self):
        # 如果没有达到节点要求， 会抛出异常 MultipleRedlockException
        self.lock = self.dlm.lock(self.key, self.timeout)

    def __unlock(self):
        # 释放失败，也会抛出 MultipleRedlockException
        self.dlm.unlock(lock=self.lock)

    def __enter__(self):
        return self.__lock()

    def __exit__(self, exc_type, exc_val, exc_tb):
        # TODO 异常处理
        return self.__unlock()
