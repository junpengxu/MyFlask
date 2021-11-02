# -*- coding: utf-8 -*-
# @Time    : 2021/10/24 1:10 下午 
# @Author  : xujunpeng
from gevent import monkey

monkey.patch_all()

from app import create_app, db
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