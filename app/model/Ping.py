# -*- coding: utf-8 -*-
# @Time    : 2021/11/11 9:17 下午 
# @Author  : xujunpeng
from app.base.base_model import BaseModel, db


class Ping(db.Model, BaseModel):
    __tablename__ = 'ping'

    desc = db.Column(db.String(32), comment="描述", nullable=False, default="")

    def simple_info(self):
        return {
            "id": self.id,
            "desc": self.desc,
            "create_time": self.create_time.strftime("%Y年%m月%d日 %H时%M分%S秒"),
            "update_time": self.update_time.strftime("%Y年%m月%d日 %H时%M分%S秒")
        }
