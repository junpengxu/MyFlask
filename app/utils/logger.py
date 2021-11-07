# -*- coding: utf-8 -*-
# @Time    : 2021/10/24 1:49 下午 
# @Author  : xujunpeng
import traceback

from app.base.base_logger import BaseLogger
from sentry_sdk import capture_exception

request_log = BaseLogger('request.log', level="INFO").logger.info
err_log = BaseLogger('err.log', level="ERROR").logger.error


def log_exception():
    err_log.error(traceback.format_exc())
    capture_exception()
