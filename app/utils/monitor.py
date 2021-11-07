# -*- coding: utf-8 -*-
# @Time    : 2021/11/3 11:20 下午 
# @Author  : xujunpeng

import time
from functools import wraps
from app.utils.GrafanaTransport import GrafanaTransport
from app.utils.logger import log_exception


# from celery.contrib import rdb
# rdb.set_trace()


def dispatch_monitor(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        st = time.time()
        try:
            t = func(self, *args, **kwargs)
        except Exception as e:
            raise e
        finally:
            # 这里是否要异步去做？
            uri = self.request.path
            endpoint = self.request.url_rule.endpoint
            method = self.request.method
            duration = int((time.time() - st) * 1000)
            if duration > 3000:
                try:
                    raise RuntimeError
                except Exception as e:
                    log_exception()

        GrafanaTransport().send(
            measurement="api_monitor",
            tags={"uri": uri, "req_m": method, 'endpoint': endpoint},
            fields={"duration": duration}
        )
        return t

    return wrapper


def celery_monitor(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        st = time.time()
        try:
            func(*args, **kwargs)
        except Exception as e:
            pass
            # log_exception()
        finally:
            duration = int((time.time() - st) * 1000)
            if duration > 3000:
                pass
        GrafanaTransport().send(
            measurement="celery_monitor",
            tags={"m_name": args[0].__name__,
                  "cn_name": getattr(args[0], "cn_name", __name__)
                  },
            fields={"duration": duration}
        )

    return wrapper
