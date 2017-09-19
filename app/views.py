# coding:utf-8
from . import app, db
import json
import datetime
from flask import render_template, request, session, redirect, url_for, current_app, flash
from lib.decorators import requireLogin
from lib.utils import serialize
from lib.login import loginUser, logoutUser, getUserId, isAdmin
from models import *

"""
-------------------------------------------------
   File Name：     views
   Description : 路由视图文件
   Author :       NvRay
   date：          2017/8/24
-------------------------------------------------
"""
__author__ = 'NvRay'


# TODO 添加默认变量和类似current_user ,用于显示个人信息等


@app.route("/")
@requireLogin
def home():
    return render_template("index.html")


@app.route("/test")
def test():
    # print current_myvar

    return "test page "


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        print request.form
        username = request.form.get("username", "")
        password = request.form.get("passwd", "")
        user = Users.query.filter_by(username=username).first()
        if user and user.checkPwd(password):
            loginUser(user)
            return redirect(url_for("home"))
        else:
            return redirect(url_for("login"))
    return render_template("login.html")


@app.route("/logout")
@requireLogin
def logout():
    logoutUser()
    return redirect("/login")


@app.route("/admin")
@requireLogin
def admin():
    return "into inner"


@app.route("/user")
@requireLogin
def user():
    # 用户管理，显示用户列表
    department_result = Department.query.all()
    return render_template("user.html", department_result=department_result)


@app.route("/department")
@requireLogin
def department():
    return render_template("department.html")


@app.route("/taskinfo")
@requireLogin
def taskinfo():
    return render_template("taskinfo.html")


@app.route("/addtask",methods=["GET","POST"])
@requireLogin
def addtask():
    if request.method == "GET":
        userData= db.session.query(Users.name, Users.id).all()
        itemData= db.session.query(Item.name, Item.id).all()
        departmentData = db.session.query(Department.name, Department.id).all()
        user_data = userData
        item_data = itemData
        department_data = departmentData
        return render_template('addtask.html', user_data=user_data, item_data=item_data, department_data=department_data,
                    task_data=[{}])
    else:
        inputid = getUserId()
        subject = request.form.get("subject")
        userid = int(request.form.get("userid"))
        assistid = int(request.form.get("assistid"))
        itemid = int(request.form.get("itemid"))
        priority = int(request.form.get("priority"))
        departmentid = int(request.form.get("departmentid"))
        startdate = request.form.get("startdate")
        enddate = request.form.get("enddate")
        content = request.form.get("content")

        # 判断表单选的userid是否大于99999，如果大于，就把这个值存到depid字段中，并把userid设成-2，表示末指定
        if userid > 99999:
            depid = userid
            userid = -2
        else:
            depid = -2

        # 判断表单选的assistid是否大于99999，如果大于，就把这个值存到dassdepid字段中，并把assistid设成-2，表示末指定
        if assistid > 99999:
            assdepid = assistid
            assistid = -2
        else:
            assdepid = -2
        def toDatetime(string):
            return datetime.datetime.strptime(string, '%Y-%m-%d')
        startdate = toDatetime(startdate)
        enddate = toDatetime(enddate)
        task = Task(inputid=inputid,subject=subject,userid=userid,depid=depid,assistid=assistid,assdepid=assdepid,itemid=itemid,priority=priority,departmentid=departmentid,startdate=startdate,enddate=enddate,content=content)
        # data = (inputid, subject, userid, depid, assistid, assdepid, itemid, priority, departmentid, startdate, enddate,
        #         content)

        db.session.add(task)
        db.session.commit()
        # result = writeDb(sql, data)
        result = 1
        if result:
            return redirect(url_for('taskinfo'))
        else:
            return '添加失败'





@app.route("/mytask")
@requireLogin
def mytask():
    return render_template("mytask.html")


@app.route("/mysendtask")
@requireLogin
def mysendtask():
    return render_template("mysendtask.html")


@app.route("/droptask")
@requireLogin
def droptask():
    return render_template("droptask.html")


@app.route("/item")
@requireLogin
def item():
    return render_template("item.html")


@app.route("/additem")
@requireLogin
def additem():
    # TODO 报错
    return render_template("additem.html")


@app.route("/dropitem")
@requireLogin
def dropitem():
    # TODO 报错
    return render_template("dropitem.html")


@app.route("/adduser", methods=["POST"])
def adduser():
    if not isAdmin():
        return "-1"
    p = request.form
    access = p.get("access")
    birthday = p.get("birthday")
    department = p.get("department")
    email = p.get("email")
    name = p.get("name")
    passwd = p.get("passwd")
    phone = p.get("phone")
    qq = p.get("qq")
    sex = p.get("sex")
    username = p.get("username")
    users = Users(access=access,
                  birthday=birthday,
                  department=department,
                  email=email,
                  name=name,
                  password=passwd,
                  phone=phone,
                  qq=qq,
                  sex=sex,
                  username=username,
                  adddate=datetime.datetime.now())
    db.session.add(users)
    db.session.commit()
    return "0"


# 操作
@app.route("/changeuser/<int:uid>",  methods=["POST"])
@requireLogin
def changeuser(uid):
    cuid = getUserId()
    p = request.form
    access = p.get("access")
    birthday = p.get("birthday")
    department = p.get("department")
    email = p.get("email")
    name = p.get("name")
    passwd = p.get("passwd")
    phone = p.get("phone")
    qq = p.get("qq")
    sex = p.get("sex")
    username = p.get("username")
    user = Users.query.filter_by(id=uid).first()
    if not user:
        return "-1"

    if uid == cuid or isAdmin():
        user.access = access
        user.birthday = birthday
        user.department = department
        user.email = email
        user.name = name
        user.password = passwd
        user.phone = phone
        user.qq = qq
        user.sex = sex
        user.username = username
        user.adddate = datetime.datetime.now()
        db.session.add(user)
        db.session.commit()
        status = "0"
    else:
        status = "-1"
    return status


# Api 接口
@app.route("/api/getuser", methods=["GET", "POST"])
@requireLogin
def apiGetuser():
    infos = db.session.query(Users.id, Users.name, Users.username, Users.birthday, Users.sex, Users.qq, Users.email,
                             Department.name, Users.phone, Users.access, Users.adddate).join(Department,
                                                                                             Users.department == Department.id).all()
    userlists = []
    for info in infos:
        userlist = {
            "id": info[0],
            "name": info[1],
            "username": info[2],
            "birthday": info[3],
            "sex": info[4],
            "qq": info[5],
            "email": info[6],
            "department": info[7],
            "phone": info[8],
            "access": info[9],
            "adddate": datetime.datetime.strftime(info[10], '%Y-%m-%d %H:%M:%S')
        }
        userlists.append(userlist)
    return json.dumps(userlists)


@app.route("/deluser", methods=["POST"])
@requireLogin
def deluser():
    if not isAdmin(): return "-1"
    uid = request.form.get("str", "")
    uids =  map(int,filter(lambda x:True if x else False,uid.split(",")))
    for u in uids:
        user = Users.query.filter_by(id= u).first()
        if int(user.id) == int(getUserId()):
            return "-1"
        db.session.delete(user)
    db.session.commit()
    return "0"


@app.route("/api/getdepartment", methods=["POST"])
def apiGetDepartment():
    queryData = Department.query.all()
    departmentLists = [serialize(col) for col in queryData]
    return json.dumps(departmentLists)

@app.route("/api/gettask", methods=["POST"])
def apiGetTask():
    # queryData = db.session.query(Task.id,Task.subject,Task.inputid,Task.userid,Task.assdepid,Task.itemid,Task.departmentid,Task.priority,Task.status,Task.startdate,Task.enddate).all()
    queryData = Task.query.all()
    print queryData[0]
    taskLists = [serialize(col) for col in queryData]
    print taskLists
    return json.dumps(taskLists)


