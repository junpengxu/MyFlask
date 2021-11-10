# -*- coding: utf-8 -*-
# @Time    : 2021/10/24 3:14 下午 
# @Author  : xujunpeng
import time
from functools import wraps
from app.enum.status_code import Codes


def login_check(func):
    @wraps(func)
    def wrapper(self, *args, **kw):
        if not self.user_id:
            return self.formattingData(code=Codes.NOT_LOG_IN)
        return func(self, *args, **kw)
    return wrapper


def monitor(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        st = time.time()
        t = func(self, *args, **kwargs)
        uri = self.request.path
        method = self.request.method
        duration = int((time.time() - st) * 1000)
        return t

    return wrapper
