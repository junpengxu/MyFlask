# -*- coding: utf-8 -*-
# @Time    : 2021/10/24 1:13 下午 
# @Author  : xujunpeng
import os
from app import app
from celery import Celery
from config import celery_config
from flask import Config


# TODO 是否要和celery的配置合并到一起呢


def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=celery_config.CELERY_RESULT_BACKEND,
        broker=celery_config.CELERY_BROKER_URL,
    )
    celery.conf.update(Config(os.getcwd()).from_object(celery_config))

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


celery = make_celery(app)
