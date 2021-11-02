# -*- coding: utf-8 -*-
# @Time    : 2021/10/24 1:49 下午 
# @Author  : xujunpeng
from app import app
from app.base.base_logger import BaseLogger

request_log = BaseLogger('request.log', level="INFO").logger.info
err_log = BaseLogger('err.log', level="ERROR").logger.error
