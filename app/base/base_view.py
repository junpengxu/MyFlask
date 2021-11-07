# -*- coding: utf-8 -*-
# @Time    : 2021/10/24 1:15 下午 
# @Author  : xujunpeng

from app import app
from flask import request, jsonify
from flask.views import MethodView
from app.utils.logger import request_log
from app.base.base_enum import BaseEnum
from app.enum.status_code import Codes
from sentry_sdk import capture_exception

from app.utils.monitor import dispatch_monitor


class BaseView(MethodView):
    def __init__(self, *args, **kwargs):
        self.__setattr__('request', request)
        self.__setattr__('user_id', self.get_user_id())
        request_log(msg="this is info,args={},data={}".format(self.request.args.to_dict(),
                                                              {} if not self.request.data else self.request.json))
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
