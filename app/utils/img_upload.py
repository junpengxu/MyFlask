# -*- coding: utf-8 -*-
# @Time    : 2021/11/2 8:18 下午 
# @Author  : xujunpeng
import abc
import uuid

import upyun
import requests

from app import app
from datetime import datetime


class UploadBase(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def gen_file_name(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def upload(self, *args, **kwargs):
        pass

    def _gen_file_name(self, *args, **kwargs):
        # 统一使用webp
        return "/{}{}".format(
            uuid.uuid4().hex,
            datetime.now().strftime("%Y%m%d"),
        )

    def read_img_from_stream(self, file_obj):
        raise NotImplemented

    def read_img_from_url(self, url):
        raise NotImplemented

    def read_img_from_path(self, path):
        raise NotImplemented


class UpYunImgUpload(UploadBase):
    def __init__(self):
        self.cli = upyun.UpYun(
            app.config['UP_SERVER'],
            username=app.config['UP_CLIENT_KEY'],
            password=app.config['UP_CLIENT_SECRET'],
            timeout=60, endpoint=upyun.ED_AUTO
        )

    def gen_file_name(self, business):
        return "/{}/{}/{}{}".format(
            app.config["UP_IMG_BUCKET"],
            business,
            uuid.uuid4().hex,
            datetime.now().strftime("%Y%m%d"),
        )

    def upload(self, business):
        """
        试试写个闭包玩
        e.g upload("business")("filestream") # return full filename
        :param business:
        :type business:
        :return:
        :rtype:
        """

        def _upload(file_stream):
            file_name = self.gen_file_name(business)
            self.cli.put(file_name, file_stream)
            return app.config["UP_SERVER_DOMAIN"] + file_name

        return _upload

    def read_img_from_url(self, url):
        return requests.get(url).content
