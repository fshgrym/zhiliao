#!/usr/bin/env python
# -*- coding:utf-8 -*- 
# Author:fsh
#日志文件
import os
from datetime import timedelta
DEBUG=True
#session
SECRET_KEY=os.urandom(24)
PERMANENT_SESSION_LIFETIME=timedelta(days=7)
#数据库
DIALECT='mysql'
DRIVER='pymysql'
USERNAME='root'
PASSWORD='123456'
HOST='127.0.0.1'
PORT='3306'
DATABASE='db_zhiliao'
SQLALCHEMY_DATABASE_URI='{}+{}://{}:{}@{}:{}/{}?charset:utf8'.format(DIALECT,DRIVER,USERNAME,PASSWORD,HOST,PORT,DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS=False