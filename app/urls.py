# -*- coding: utf-8 -*-
# @Time    : 2021/10/24 1:14 下午 
# @Author  : xujunpeng

from app.view.ping import Ping
def bind_urls(app):
    app.add_url_rule('/ping', view_func=Ping.as_view('乒'), methods=['GET', 'POST'])