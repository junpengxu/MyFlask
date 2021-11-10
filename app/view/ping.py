# -*- coding: utf-8 -*-
# @Time    : 2021/10/24 1:40 下午 
# @Author  : xujunpeng
import time

from app.base.base_view import BaseView
from app.utils.decorator import login_check
from app.enum.status_code import Codes
from app.celery.tasks import ping
from app.controller.Ping import PingController


class Ping(BaseView):
    def get(self):
        for i in range(10):
            time.sleep(0.5)
            print("doing")
            ping.delay()
            data = PingController.get(123)
        return self.formattingData(code=Codes.SUCCESS, data=data)

    @login_check
    def post(self):
        return self.formattingData(code=Codes.SUCCESS)
