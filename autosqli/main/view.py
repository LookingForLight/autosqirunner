#-*-coding:utf-8-*-
from flask import Flask, render_template, url_for, request, redirect,abort,jsonify
from .form import MyForm,AutosqliForm,TaskInfo
from . import sqil
from ..core.autosqli import Client
import json
from datetime import datetime
from ..config import Conf
import re
from utils.mod_db import database
from datetime import datetime
from flask_paginate import Pagination,get_page_parameter
from utils.mod_db import sqlalchemy_op
import math


client = Client(Conf.sqlmap_server, Conf.sqlmap_port, admin_token=Conf.admin_token)
db=sqlalchemy_op()

@sqil.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        form = MyForm()
    if request.method == 'POST':
        form = MyForm(request.form)
        if form.validate_on_submit():
            return redirect('http://www.baidu.com')
        else:
            print(form.errors)
    return render_template('admin/login.html', form = form)


@sqil.route('/',methods=['GET'])
def index():
    db = sqlalchemy_op()

    page_size = 10
    total =db._session.query(TaskInfo).count()
    totalpage = math.ceil(total/page_size)
    page = int(request.args.get('page'))
    if page == 1:
        start = 0
        end = page_size
    elif page >1:
        start = (page-1) * page_size
        end = start+page_size
    tasksinfo = db._session.query(TaskInfo).order_by(TaskInfo.id.desc()).slice(start,end)
    records = []
    if tasksinfo:
        for taskinfo in tasksinfo:
            info = {"taskid": taskinfo.taskid, "status": taskinfo.status, "id": taskinfo.id,
                    "createtime": taskinfo.createtime}
            records.append(info)
        return jsonify(
            {
                "tasks_num": total,
                'success': 'true',
                'records': records,
                "totalpage":totalpage
            }
        )


@sqil.route('/home',methods=['GET', 'POST'])
def autosqli():

    if request.method == 'GET':
        form = AutosqliForm()
    if request.method == 'POST':
        form = AutosqliForm(request.form)
        if form.validate_on_submit():
            url = form.test_url.data
            method = form.request_method.data
            request_params = form.request_params.data
            ignore_params = form.ignore_params.data

            send_params = "url : {0},\nmethod :{1},\nrequest_params :{2},\nignore: {3}".format(url,method,request_params,ignore_params)
            print(send_params)
            return redirect('http://www.baidu.com')
        else:
            print(form.errors)
    return render_template('autosqli/demo.html', form = form)


@sqil.route('/index',methods=['GET'])
def home():

    if request.method == 'GET':
        return render_template('autosqli/index.html')


@sqil.route('/recordlist',methods=['GET'])
def recordlist():

    page = int(request.args.get('page'))
    tasksinfo = paginate_data(page)
    records = []
    if tasksinfo['tasksinfo']:
        for taskinfo in tasksinfo['tasksinfo']:
            taskstatus = client.get_taskid_status(taskinfo.taskid)
            if taskstatus != taskinfo.status:
                db._session.query(TaskInfo).filter(TaskInfo.taskid == taskinfo.taskid).update({"status": taskstatus})
            info = {"taskid": taskinfo.taskid, "status": taskstatus, "id": taskinfo.id,
                    "createtime": taskinfo.createtime.strftime("%Y-%m-%d %H:%M:%S")}
            records.append(info)
    db._session.commit()
    db._session.close()
    return jsonify(
            {
                "tasks_num": tasksinfo['total'],
                'success': 'true',
                'records': records,
                "totalpage":tasksinfo['totalpage']
            }
        )

@sqil.route('/addrecord',methods=['POST'])
def addrecord():

    if not request.json:
        abort('400')

    options = request.json
    print(options)
    if not check_url(options['url']):
       return jsonify({
           "code": "0002",
           "message": "url格式不正确"
       })

    if options['method'] == 'GET' and options['data']:
        for key,value in json.loads(options['data']).items():
            options[key] = value
        del options['data']
    elif options['method'] == 'GET' and not options['data']:
        del  options['data']

    taskid = client.create_new_task()
    insert_task(taskid)
    print(options)

    flag = client.set_taskid_options(taskid,options)

    if flag:
        print("设置成功")
        return jsonify({
            "code":"0000",
            'taskid':taskid,
            "message":"创建成功:"+taskid
        })
    else:
        return jsonify({
            "code":"0005"
        })

@sqil.route('/saverecord/<taskid>', methods=['POST'])
def saverecord(taskid):

    if not request.json:
        abort('400')
    options = request.json
    flag = client.set_taskid_options(taskid,options)

    if flag:
        print("保存成功")
        return jsonify({
            "code":"0000",
            "message":"编辑保存成功:"+taskid
        })

@sqil.route('/delrecord/<taskid>',methods=['GET'])
def delrecord(taskid):
    status = client.del_a_task(taskid)
    if status:
        return jsonify({

            "code":"0000",
            "message":"删除成功:"+taskid
        })
    else:
        return jsonify({

            "code":"0001",
            "message":"删除失败:"+taskid
        })

@sqil.route('/actrecord/<taskid>',methods=['GET'])
def actrecord(taskid):
    result = client.start_taskid_scan(taskid)

    if result:
        update_status(taskid)

    return jsonify(result)
@sqil.route('/getresult/<taskid>',methods=['GET'])
def getresult(taskid):
    result = client.get_result(taskid)

    if result:

        return jsonify({

            "code":'0000',
            "result":result,
            "message":"获取成功"
        })
    else:
        return jsonify({

            "code": '0000',
            "result": "无注入漏洞",
            "message": "获取成功"
        })

@sqil.route('/getlog/<taskid>',methods=['GET'])
def getlog(taskid):
    result = client.get_scan_log(taskid)

    if result:

        return jsonify({

            "code":'0000',
            "result":result,
            "message":"获取成功"
        })
    else:
        return jsonify({

            "code": '0000',
            "result": "查无日志",
            "message": "获取成功"
        })

@sqil.route('/getoptionlist/<taskid>',methods=['GET'])
def get_option_list(taskid):
    option_list = client.get_taskid_options(taskid)
    return jsonify(option_list)

@sqil.route('/taskinfo',methods=['GET'])

def taskinfo():
    """
       sql注入demo接口
    """
    id = request.args.get('id')
    res = sqli_demo(id)
    result = []
    for re in res:
        taskinfo = {"id":re[0],"taskid":re[1]}
        result.append(taskinfo)
    return jsonify({

        "result":result
    })

def check_url(url):

    compiler = re.compile(r'^(http|https)://')
    if compiler.match(url):
        return True
    else:
        return False


def check_switch_data(data):
    try:
        data = json.loads(data)
        data.items()
    except Exception as e:
        return False
    else:
        return True

def status_cn(status):
    status_cn = "待运行"
    if status == "not running":
        status_cn= "待运行"
    elif status == "running":
        status_cn="正在运行"
    elif status =="terminated":
        status_cn = "运行结束"
    return status_cn

def task_list():
    sql = "select * from taskinfo order by id desc "
    db = database()
    rows = db.select_data(sql)
    db._conn.close()
    return list(rows)

def insert_task(taskid):
    sql = """insert into taskinfo(taskid,status) value (%s,"not running")"""
    db = database()
    db._cursor.execute(sql,taskid)
    db._conn.commit()
    db._conn.close()

def paginate_data(page=1,page_size=10):

    page_size = page_size
    total = db._session.query(TaskInfo).count()
    totalpage = math.ceil(total/page_size)
    page = page
    if page == 1:
        start = 0
        end = page_size
    elif page >1:
        start = (page-1) * page_size
        end = start+page_size
    tasksinfo = db._session.query(TaskInfo).order_by(TaskInfo.id.desc()).slice(start,end)
    return {
        "tasksinfo":tasksinfo,
        "totalpage":totalpage,
        "total":total
    }

def update_status(taskid):
    db._session.query(TaskInfo).filter(TaskInfo.taskid==taskid).update({"status":"runnning"})
    db._session.commit()
    db._session.close()

def sqli_demo(id):
    mydb = database()
    sql = "select * from sqlimap.taskinfo where id = %s " % (id)
    print(sql)
    mydb._cursor.execute(sql)

    rows = mydb._cursor.fetchall()
    mydb._conn.close()

    return rows