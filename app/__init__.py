# -*- coding: utf-8 -*-
# @Time    : 2021/10/24 1:10 下午 
# @Author  : xujunpeng
import sentry_sdk
import config as app_config
from flask import Flask, request, g
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.celery import CeleryIntegration
from py_zipkin.util import ZipkinAttrs, generate_random_64bit_string, create_attrs_for_span

sentry_sdk.init(
    dsn=app_config.SENTRY_DSN,
    integrations=[FlaskIntegration(), CeleryIntegration()]
)
app = Flask(__name__)
app.config.from_object(app_config)


def create_app():
    from app.urls import bind_urls
    bind_urls(app)
    return app


@app.after_request
def after_request(response):
    return response


@app.before_request
def before_request():
    # 判断请求的request中是否含有trace信息
    trace_id = request.headers.get("trace_id")
    span_id = request.headers.get("span_id")
    is_sampled = request.headers.get("is_sampled")
    flags = request.headers.get("flags")
    if trace_id and span_id:
        trace = ZipkinAttrs(
            span_id=generate_random_64bit_string(),
            trace_id=trace_id,
            flags=flags,
            parent_span_id=span_id,
            is_sampled=is_sampled
        )
    else:
        trace = create_attrs_for_span()
    setattr(g, app.config["ZIPKIN_TRACE"], trace)
