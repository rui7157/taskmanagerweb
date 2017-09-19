# coding:utf-8
import os

"""
-------------------------------------------------
   File Name：     config
   Description : 主配置文件
   设置环境变量“flaskenv”使用相应配置类,或者手动修改MYENV变量

   Author :       NvRay
   date：          2017/8/24
-------------------------------------------------
"""
__author__ = 'NvRay'
__all__ = ["config"]
currentPath = os.path.dirname(__file__)
MYENV = "dev"
#TODO  严重的配置问题可定制性不足

class Config:
    """公共配置"""
    curPath = currentPath
    SECRET_KEY = "96bbca95e43a958f8feabd62408759eb"


class TestEvn(Config):
    """测试环境"""


class MainEvn(Config):
    """生产环境"""
    # mysql
    # mysql + pymysql: // user:password @ ip:port / db_name


class DevEvn(Config):
    """开发环境"""
    # 数据库信息
    # SQLite
    testVar = "testData"
    SQLALCHEMY_DATABASE_URI = "sqlite:///{}".format(os.path.join(Config.curPath, "..","database.db"))
    SQLALCHEMY_TRACK_MODIFICATIONS = True


# 决定环境

configData = {
    "test": TestEvn,
    "main": MainEvn,
    "dev": DevEvn,
}


def getEnvConfig():
    if not MYENV:
        env = os.environ.get("flaskenv", "dev")
    else:
        env = MYENV
    return configData.get(env)


config = getEnvConfig()
