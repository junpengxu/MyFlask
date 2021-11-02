# -*- coding: utf-8 -*-
# @Time    : 2021/10/24 1:10 下午 
# @Author  : xujunpeng

from flask import Flask
import config as app_config
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.celery import CeleryIntegration

sentry_sdk.init(
    dsn=app_config.SENTRY_DSN,
    integrations=[FlaskIntegration(), CeleryIntegration()]
)

app = Flask(__name__)
app.config.from_object(app_config)

from app.base.base_model import db


def create_app():
    from app.urls import bind_urls
    bind_urls(app)
    return app
