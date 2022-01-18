# -*- coding: utf-8 -*-
# @Time    : 2021/10/24 1:15 下午 
# @Author  : xujunpeng
from datetime import datetime
import random
from app import app
from flask_sqlalchemy import SQLAlchemy, BaseQuery, SignallingSession, get_state
from sqlalchemy import orm
from app.utils.trace import Trace


class QueryWithSoftDelete(BaseQuery):
    _with_deleted = False

    def __new__(cls, *args, **kwargs):
        obj = super(QueryWithSoftDelete, cls).__new__(cls)
        obj._with_deleted = kwargs.pop('_with_deleted', False)
        if len(args) > 0:
            super(QueryWithSoftDelete, obj).__init__(*args, **kwargs)
            return obj.filter_by(delete=False) if not obj._with_deleted else obj
        return obj

    def __init__(self, *args, **kwargs):
        pass

    def with_deleted(self):
        return self.__class__(self._only_full_mapper_zero('get'),
                              session=db.session(), _with_deleted=True)

    def _get(self, *args, **kwargs):
        # this calls the original query.get function from the base class
        return super(QueryWithSoftDelete, self).get(*args, **kwargs)

    @Trace
    def get(self, *args, **kwargs):
        # the query.get method does not like it if there is a filter clause
        # pre-loaded, so we need to implement it using a workaround
        obj = self.with_deleted()._get(*args, **kwargs)
        return obj if obj is None or self._with_deleted or not obj.delete else None


class RoutingSession(SignallingSession):

    def __init__(self, *args, **kwargs):
        self.slave_db_key = [bind.startswith("slave") for bind in app.config["SQLALCHEMY_BINDS"].keys()]
        super(RoutingSession, self).__init__(*args, **kwargs)

    def get_bind(self, mapper=None, clause=None):
        """每次数据库操作(增删改查及事务操作)都会调用该方法, 来获取对应的数据库引擎(访问的数据库)"""
        state = get_state(self.app)
        if mapper is not None:
            try:
                # SA >= 1.3
                persist_selectable = mapper.persist_selectable
            except AttributeError:
                # SA < 1.3
                persist_selectable = mapper.mapped_table
            # 如果项目中指明了特定数据库，就获取到bind_key指明的数据库，进行数据库绑定
            info = getattr(persist_selectable, 'info', {})
            bind_key = info.get('bind_key')
            if bind_key is not None:
                return state.db.get_engine(self.app, bind=bind_key)

                # 使用默认的主数据库
                # SQLALCHEMY_DATABASE_URI 返回数据库引擎
                # return SessionBase.get_bind(self, mapper, clause)

        from sqlalchemy.sql.dml import UpdateBase
        # 写操作 或者 更新 删除操作 - 访问主库
        if self._flushing or isinstance(clause, UpdateBase):
            print("写更新删除 访问主库")
            # 返回主库的数据库引擎
            return state.db.get_engine(self.app, bind="master")
        else:
            # 读操作--访问从库
            slave_key = random.choice(self.slave_db_key)
            print("访问从库:{}".format(slave_key))
            # 返回从库的数据库引擎
            return state.db.get_engine(self.app, bind=slave_key)


# 3.2 自定义RoutingSQLAlchemy，继承于SQLAlchemy，重写写create_session，替换底层的SignallingSession
# https://www.cxyzjd.com/article/user_san/109649006
class RoutingSQLAlchemy(SQLAlchemy):

    def create_session(self, options):
        # 使用自定义实现了读写分离的RoutingSession
        return orm.sessionmaker(class_=RoutingSession, db=self, **options)


# 3.3根据RoutingSQLAlchemy创建数据库对象

db = RoutingSQLAlchemy(app, use_native_unicode="utf8mb4", query_class=QueryWithSoftDelete)


class BaseModel(object):
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4'
    }
    id = db.Column(db.Integer, primary_key=True)
    create_time = db.Column(db.DateTime, default=datetime.now, index=True)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    delete = db.Column(db.Boolean, default=False)

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            raise e

    def update(self):
        try:
            db.session.merge(self)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            raise e

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        # 特殊处理一下时间
        if dict.get('create_time'):
            dict['create_time'] = dict['create_time'].strftime("%Y年%m月%d日 %H时%M分%S秒")
        if dict.get('update_time'):
            dict['update_time'] = dict['update_time'].strftime("%Y年%m月%d日 %H时%M分%S秒")
        return dict

    @staticmethod
    def save_all(model_list):
        try:
            db.session.add_all(model_list)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            raise e

    def get_detail(self):
        return {}
