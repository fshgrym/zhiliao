#!/usr/bin/env python
# -*- coding:utf-8 -*- 
# Author:fsh
#配置文件
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from zhiliao import app
from exts import db
from models import User,Question,Answer
manager=Manager(app)
migrate=Migrate(app,db)
#添加迁移脚本
manager.add_command('db',MigrateCommand)

if __name__ == '__main__':
    manager.run()