# -*- coding: utf-8 -*-
# @Time    : 2021/10/24 1:15 下午 
# @Author  : xujunpeng
import json
import time

from app import app
from flask import request, jsonify
from flask.views import MethodView
from app.utils.logger import request_log
from app.base.base_enum import BaseEnum
from app.enum.status_code import Codes
from sentry_sdk import capture_exception
from app.utils.trace import Trace, TraceDecorator
from app.utils.monitor import dispatch_monitor
from app.utils.kafka import KafkaProducer
from functools import wraps

# def dispatch_func_name(func):
#     @wraps(func)
#     def wrap(*args, **kwargs):
#         # 修改函数名字
#         func.__module__ = args[0].__module__
#         func.__name__ = request.method.lower()
#         return func(*args, **kwargs)
#     return wrap


class BaseView(MethodView):
    def __init__(self, *args, **kwargs):
        self.__setattr__('request', request)
        self.__setattr__('user_id', self.get_user_id())
        request_log(msg="this is info,args={},data={}".format(self.request.args.to_dict(),
                                                              {} if not self.request.data else self.request.json))
        # 执行trace压栈的操作
        log = {
            "user_id": self.user_id,
            "session_id": "",
            "server_name": "MyFlask",
            "timestamp": int(time.time() * 1000),
            "ip": self.request.headers.get("X-Real-IP"),
            "request_url": self.request.path,
            "request_method": self.request.method,
            "request_endpoint": self.request.url_rule.endpoint,
            "request_args": self.request.args.to_dict(),
            "request_params": {} if not self.request.data else self.request.json,
        }

        KafkaProducer.produce(topic=app.config["KAFKA_LOGS_TOPIC"], value=json.dumps(log))
        super(BaseView, self).__init__(*args, **kwargs)

    def formattingData(self, code, msg=None, data=None):
        if isinstance(code, BaseEnum):
            if not msg:
                msg = code.desc
            code = code.code
        return jsonify(
            {
                "code": code,
                "message": msg,
                "data": data
            }
        )


    @dispatch_monitor
    @Trace
    def dispatch_request(self, *args, **kwargs):
        try:
            # 白名单
            if self.request.url_rule.rule in app.config["WHITE_URL_LIST"]:
                print("hit white list")
            # 黑名单
            elif self.request.url_rule.rule in app.config["BLACK_URL_LIST"]:
                print("hit black list")
            # 正常处理的请求
            else:
                print("normal request")

            # post 请求的特殊处理
            if self.request.method == "POST":
                pass
            return super(BaseView, self).dispatch_request(*args, **kwargs)
        except Exception as e:
            capture_exception()
            return self.formattingData(Codes.FAIL)

    def get_user_id(self):
        return 0
