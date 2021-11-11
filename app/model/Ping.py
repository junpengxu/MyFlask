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
        }
