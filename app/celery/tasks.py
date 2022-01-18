# -*- coding: utf-8 -*-
# @Time    : 2021/10/31 3:09 下午 
# @Author  : xujunpeng

from app.celery import celery
from app.controller.Ping import PingController

@celery.task(cn_name="测试ping")
def ping():
    PingController().create(desc="123")
    PingController().get(1)
    PingController().get(1)
    PingController().get(1)
    print("ping ! finish    ")
