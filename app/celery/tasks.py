# -*- coding: utf-8 -*-
# @Time    : 2021/10/31 3:09 下午 
# @Author  : xujunpeng
from app.celery import celery


@celery.task
def ping():
    print("ping !")
    raise RuntimeError
