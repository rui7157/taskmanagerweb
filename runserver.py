#coding:utf-8
from flask_script import Shell
from flask_migrate import Migrate,MigrateCommand

from app import application,manager,models,db
__author__ = 'NvRay'

"""
-------------------------------------------------
   File Name：     runserver
   Description :
   Author :       NvRay
   date：          2017/8/24
-------------------------------------------------
"""

def createAdmin():
    from datetime import datetime
    datetime.now()
    now = datetime.now()
    if models.Users.query.filter_by(username = "admin").first():
        print "The 'admin' already exists"
        return
    adminUser  = models.Users(name="administrator",username = "admin",password = "admin",phone=12233,birthday="ddd",sex=1,qq=123123,email = "ddd",department = 1, access = 1, image = "sdd", adddate = now, status = 1)
    db.session.add(adminUser)
    db.session.commit()

def runServer():
    application.run("127.0.0.1",5500,debug=True)

def createDB():
    db.create_all()


# TODO 迁移问题
migrate = Migrate(application,db)
commands = {
    "createadmin":Shell(make_context=createAdmin),
    "runserver":Shell(make_context=runServer),
    "createdb":Shell(make_context=createDB),
    "db":MigrateCommand
}

[manager.add_command(*(cmd,func)) for cmd,func in commands.items()]

if __name__ == '__main__':
    import os
    if os.environ.get("PYTHONUNBUFFERED"):
        #IDE开发环境
        runServer()
        # manager.run()
    else:
        manager.run()
