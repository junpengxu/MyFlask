# -*- coding: utf-8 -*-
# @Time    : 2021/10/24 1:10 下午 
# @Author  : xujunpeng
from gevent import monkey

monkey.patch_all()
import app.model  # 用于引入所有的model，防止生成sqlarchmy找不到模型, 需要找一个更加优雅的方式
from app import create_app
from app.base.base_model import db

from flask_migrate import Migrate, MigrateCommand
from flask_script import Shell, Manager, Server

app = create_app()
manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)
manager.add_command('db-upgrade', MigrateCommand)
manager.add_command("runserver", Server(host=app.config["SERVER_HOST"], port=app.config['SERVER_PORT'],
                                        use_debugger=app.config["SERVER_DEBUG"]))
manager.add_command("shell", Shell())

if __name__ == '__main__':
    manager.run()
