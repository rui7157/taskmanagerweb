# coding:utf-8
from hashlib import md5
from sqlalchemy.orm import class_mapper
# from flask import current_app
from .. import app
import datetime

"""
-------------------------------------------------
   File Name：     utils
   Description : 各种需要的工具
   Author :       NvRay
   date：          2017/8/28
-------------------------------------------------
"""
__author__ = 'NvRay'


def hashPwd(pwd):
    # 密码加密
    pwd = pwd.encode("utf-8")
    pwdData = md5()
    print app.config.__dict__
    salt = app.config.get("SECRET_KEY","nvray-suijizifuchuan")
    pwdData.update(pwd)
    pwdData.update(salt)
    md5pwd = pwdData.hexdigest()
    return md5pwd


def chkPwd(md5pwd, pwd):
    # 密码校验
    # TODO v2和v3兼容 str
    # if isinstance(pwd1, str):
    #     pwd1 = pwd1.encode("utf-8")
    if isinstance(pwd, str):
        pwd = pwd.encode("utf-8")

    return md5pwd == hashPwd(pwd)



def serialize(model):
    """从model取值转换kv形式
    serialized_labels = [
      serialize(label)
      for label in session.query(LabelsData)
    ]
    """
    columns = [c.key for c in class_mapper(model.__class__).columns]

    jsonData = {}
    for c in columns:
        if isinstance(getattr(model,c),datetime.datetime):
            jsonData[c] = str(getattr(model, c))
        else:
            jsonData[c] = getattr(model, c)
    return jsonData


if __name__ == "__main__":

    print hashPwd("123")
