# -*- coding: utf-8 -*-
# @Time    : 2021/10/24 1:40 下午 
# @Author  : xujunpeng
from app.base.base_view import BaseView
from app.utils.decorator import login_check
from app.celery.tasks import ping
from app.enum.status_code import Codes
from app.controller.Ping import PingController


class Ping(BaseView):

    def get(self):

        params = self.request.args
        pk = params.get("pk", 1)
        ping.delay()
        res = PingController().get(pk)
        return self.formattingData(code=Codes.SUCCESS, data=res)

    @login_check
    def post(self):
        params = self.request.json
        desc = params.get("desc")
        PingController().create(desc=desc)
        return self.formattingData(code=Codes.SUCCESS)
