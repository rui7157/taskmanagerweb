#coding:utf-8
from flask import session,_app_ctx_stack
from ..models import Users
"""
-------------------------------------------------
   File Name：     login

   Description :    给已登陆用户设定状态
    is_authenticated 如果用户已经登录，必须返回 True ，否则返回 False
    get_id 必须返回用户的唯一标识符，使用 Unicode 编码字符串

   Author :       NvRay
   date：          2017/8/28
-------------------------------------------------
"""
__author__ = 'NvRay'


def loginUser(user,remember=False):
    """登陆
    :param user: 这是一个当前登录用户sql Model对象
    :param remember: 记住登陆选项
    """
    session["userid"] = user.id
    if remember:session["remember"] = "set"

def getUserId():
    uid = str(session.get("userid",0))
    if uid and  Users.query.filter_by(id = uid).all():
        return uid
    raise "now not anyone login user!"

def isAdmin():
    suid = int(session.get("userid", 0))
    cuser = Users.query.filter_by(id=suid).first()
    return cuser.access == 1

def logoutUser():
    #退出登陆
    ""
    if "remember" in  session:session.pop("remember")
    if "userid" in session:session.pop("userid")
