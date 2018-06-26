#!/usr/bin/env python
# -*- coding:utf-8 -*- 
# Author:fsh
from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash#generate_password_hash生成密码generate_password_hash根据原生密码进行解密
#数据库
class User(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    telephone=db.Column(db.String(11),nullable=False)
    username=db.Column(db.String(50),nullable=False)
    password=db.Column(db.String(100),nullable=False)
    def __init__(self,*args,**kwargs):#用户注册是进行拦截password
        telephone=kwargs.get('telephone')
        username=kwargs.get('username')
        password=kwargs.get('password')
        self.telephone=telephone
        self.username=username
        self.password=generate_password_hash(password)#进行加密
    def check_password(self,raw_password):
        result=check_password_hash(self.password,raw_password)
        return result
class Question(db.Model):
    __tablename__='question'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    title=db.Column(db.String(100),nullable=False)
    content=db.Column(db.Text,nullable=False)
    #now（）获取的是服务器创建的时间，now就是每次创建的时候的时间
    create_time=db.Column(db.DateTime,default=datetime.now)
    author_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    author=db.relationship('User',backref=db.backref('question'))

#评论
class Answer(db.Model):
    __tablename__='answer'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    content=db.Column(db.Text,nullable=False)
    question_id=db.Column(db.Integer,db.ForeignKey('question.id'))
    author_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    answer_time=db.Column(db.DateTime,default=datetime.now)
    question=db.relationship('Question',backref=db.backref('answers',order_by=answer_time.desc()))
    author=db.relationship('User',backref=db.backref('answers'))