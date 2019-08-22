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


client = Client(Conf.sqlmap_server, Conf.sqlmap_port, admin_token=Conf.admin_token)

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


@sqil.route('/')
def index():
    db = sqlalchemy_op()

    PER_PAGE = 10
    total =db._session.query(TaskInfo).count()
    page = request.args.get(get_page_parameter(),type=int,default=1)
    start = (page-1)*PER_PAGE
    end = start+PER_PAGE
    pagination = Pagination(bs_version=4,page=page,total=total)
    taskinfo = db._session.query(TaskInfo).order_by(TaskInfo.id.desc()).slice(start,end)

    context={
        "pagination":pagination,
        "taskinfo":taskinfo
    }
    return render_template('autosqli/bootvue2.html',**context)

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
    return render_template('autosqli/index.html',form = form)


@sqil.route('/index',methods=['GET'])
def home():

    if request.method == 'GET':
        return render_template('autosqli/bootvue.html')


@sqil.route('/recordlist',methods=['GET'])
def recordlist():


    # client = Client('10.101.52.2','8775',admin_token=' 8aee6e49c56499637ae2d6f6e6733445')

    # all_tasks = client.get_all_task_list()
    all_tasks = task_list()

    records=[]
    if all_tasks:
        for taskinfo in all_tasks:
            print(type(taskinfo[3]))
            info = {"taskid":taskinfo[1],"status":taskinfo[2],"id":taskinfo[0],"createtime":taskinfo[3].strftime("%Y-%m-%d %H:%M:%S")}
            records.append(info)
        return jsonify(
            {
                "tasks_num":len(all_tasks),
                'success':'true',
                'records':records
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
        result.setdefault('startTime',datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
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


