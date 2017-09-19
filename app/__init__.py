# coding:utf-8
from flask import Flask
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy

from config import config

"""
-------------------------------------------------
   File Name：     __init__
   Description : 应用初始化目录
   Author :       NvRay
   date：          2017/8/24
-------------------------------------------------
"""

__all__ = ["app", "db", "application"]
__author__ = 'NvRay'


app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)
manager =  Manager(app)


from views import *
application = app


