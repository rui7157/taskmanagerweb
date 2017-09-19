#coding:utf-8
from ..models import *
from functools import wraps
from flask import session,redirect,url_for,flash
"""
-------------------------------------------------
   File Name：     decorator
   Description : 装饰器函数
   Author :       NvRay
   date：          2017/8/25
-------------------------------------------------
"""
__author__ = 'NvRay'

def requireLogin(f):
    @wraps(f)
    def check(*args,**kw):
        uid = session.get("userid","")
        if not uid or not Users.query.filter_by(id = int(uid)).first():
            flash(u"请登录！")
            return redirect(url_for("login"))

        return f(*args,**kw)
    return check