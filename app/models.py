# coding:utf-8
from . import db
from lib.utils import hashPwd,chkPwd
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class ModelError(Exception):
    pass

class ForbiddenGetValue(ModelError):
    def __init__(self):
        self.__str__ = "Forbidden access the field!"




"""
-------------------------------------------------
   File Name：     models
   Description :
   Author :       NvRay
   date：          2017/8/25
-------------------------------------------------
"""
__author__ = 'NvRay'


class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(20),unique=True)
    username = db.Column(db.String(50),unique=True)
    passwd = db.Column(db.String(50))
    phone = db.Column(db.Integer())
    birthday = db.Column(db.String(20))
    sex = db.Column(db.String(4))
    qq = db.Column(db.Integer())
    email = db.Column(db.String(50))
    department = db.Column(db.Integer())
    access = db.Column(db.Integer())
    image = db.Column(db.String(50))
    adddate = db.Column(db.TIMESTAMP)
    status = db.Column(db.SmallInteger())

    @property
    def password(self, item):
        if item == "passwd":
            raise ForbiddenGetValue

    def checkPwd(self,pwd):
        #密码校验
        return chkPwd(self.passwd,pwd)

    def _safeSetPasswd(self,pwd):
        md5Passwd = hashPwd(pwd)
        self.passwd = md5Passwd

    @password.setter
    def password(self, pwd):
        md5Passwd = hashPwd(pwd)
        self.passwd = md5Passwd

    def __repr__(self):
        return "<User {}>".format(self.name)


class Task(db.Model):
    __tablename__ = "task"
    id = db.Column(db.Integer(), primary_key=True)
    inputid = db.Column(db.Integer())
    inputdate = db.Column(db.TIMESTAMP())
    userid = db.Column(db.Integer())
    depid = db.Column(db.Integer())
    assistid = db.Column(db.Integer())
    assdepid = db.Column(db.Integer())
    subject = db.Column(db.String(200))
    content = db.Column(db.Text())
    status = db.Column(db.SmallInteger(),default=0)
    startdate = db.Column(db.DateTime())
    enddate = db.Column(db.DateTime())
    begindate = db.Column(db.DateTime())
    finishdate = db.Column(db.DateTime())
    evaluate = db.Column(db.Text())
    priority = db.Column(db.SmallInteger())
    itemid = db.Column(db.Integer())
    departmentid = db.Column(db.Integer())
    del_userid = db.Column(db.Integer())
    del_status = db.Column(db.Integer(),default=1)

    def __repr__(self):
        return "<Task {}>".format(self.inputid)


class Item(db.Model):
    __tablename__ = "item"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50))
    userid = db.Column(db.Integer())
    itype = db.Column(db.String(50))
    adddate = db.Column(db.TIMESTAMP())
    startdate = db.Column(db.Date())
    enddate = db.Column(db.Date())
    content = db.Column(db.Text())
    status = db.Column(db.SmallInteger())
    del_userid = db.Column(db.Integer())
    del_status = db.Column(db.SmallInteger())

    def __repr__(self):
        return "<Item {}>".format(self.name)


class ItemReply(db.Model):
    __tablename__ = "itemreply"
    id = db.Column(db.Integer(), primary_key=True)
    userid = db.Column(db.Integer())
    content = db.Column(db.Text())
    editdate = db.Column(db.TIMESTAMP())
    taskid = db.Column(db.Integer())

    def __repr__(self):
        return "<ItemReply {}>".format(self.userid)


class TaskReply(db.Model):
    __tablename__ = "taskreply"
    id = db.Column(db.Integer(), primary_key=True)
    userid = db.Column(db.Integer())
    content = db.Column(db.Text())
    editdate = db.Column(db.TIMESTAMP())
    taskid = db.Column(db.Integer())

    def __repr__(self):
        return "<TaskReply {}".format(self.userid)


class Department(db.Model):
    __tablename__ = "department"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50))

    def __repr__(self):
        return "<Department {}>".format(self.name.encode('utf-8'))
