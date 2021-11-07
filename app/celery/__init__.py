# -*- coding: utf-8 -*-
# @Time    : 2021/10/24 1:13 下午 
# @Author  : xujunpeng
import os
from functools import wraps

from app import app
from celery import Celery

from app.utils.monitor import celery_monitor
from config import celery_config
from flask import Config


def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=celery_config.CELERY_RESULT_BACKEND,
        broker=celery_config.CELERY_BROKER_URL,
    )
    _config = Config(os.getcwd())
    _config.from_object(celery_config)
    celery.conf.update(_config)

    class ContextTask(celery.Task):
        @celery_monitor
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


celery = make_celery(app)
