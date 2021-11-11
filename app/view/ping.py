# -*- coding: utf-8 -*-
# @Time    : 2021/10/24 1:40 下午 
# @Author  : xujunpeng
from app.base.base_view import BaseView
from app.utils.decorator import login_check
from app.enum.status_code import Codes
from app.controller.Ping import PingController


class Ping(BaseView):
    def get(self):
        for i in range(1):
            # ping.delay()
            print("ping")
            PingController().get()
            PingController().query()
            PingController().create()
        return self.formattingData(code=Codes.SUCCESS, data="data")

    @login_check
    def post(self):
        return self.formattingData(code=Codes.SUCCESS)
