#-*-coding:utf-8-*-
from flask import Flask, render_template, url_for, request, redirect,abort,jsonify
from .form import MyForm,AutosqliForm
from . import sqil
from ..core.autosqli import Client
import json
from datetime import datetime
from ..config import Conf
import re

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
    return render_template('index.html')

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

    all_tasks = client.get_all_task_list()
    records=[]
    if all_tasks['success']:
        tasksinfo = all_tasks['tasks']

        for taskid,status in tasksinfo.items():
            info = {"taskid":taskid,"status":status}
            records.append(info)
        return jsonify(
            {
                "tasks_num":all_tasks['tasks_num'],
                'success':all_tasks['success'],
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
