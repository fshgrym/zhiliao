#!/usr/bin/env python
# -*- coding:utf-8 -*- 
# Author:fsh
#一般把装饰器函数放在这里
#登陆限制
from functools import wraps
from flask import session,redirect,url_for
def login_required(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        if session.get('user_id'):
            return func(*args,**kwargs)
        else:
            return redirect(url_for('login'))
    return wrapper