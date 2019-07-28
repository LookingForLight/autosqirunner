#-*-coding:utf-8-*-
from flask import Flask, render_template, url_for, request, redirect,abort,jsonify
from .form import MyForm,AutosqliForm
from . import sqil
from ..core.autosqli import Client
import json

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
    client = Client('127.0.0.1','8775',admin_token='d98e80e305f381ee3df4699924d76534')

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

    client = Client('127.0.0.1','8775',admin_token='d98e80e305f381ee3df4699924d76534')
    client.create_new_task()
    options = request.json
    if options['method'] == 'GET':
        if options['data']:

            data = json.loads(options['data'])
            print(type(data))
            del options['data']
            for key,value in data.items():
                options[key] = value
        else:
            del options['data']

    print(options)
    flag = client.set_task_options(options)

    if flag:
        print("设置成功")
        return jsonify({
            "code":"0000",
            'taskid':client.taskid
        })


@sqil.route('/delrecord/<taskid>',methods=['GET'])
def delrecord(taskid):
    client = Client('127.0.0.1','8775',admin_token='d98e80e305f381ee3df4699924d76534')
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
    client = Client('127.0.0.1','8775',admin_token='d98e80e305f381ee3df4699924d76534')
    result = client.start_taskid_scan(taskid)

    if result:
        result.setdefault('startTime',client.start_scan_time)
        return jsonify(result)

@sqil.route('/getresult/<taskid>',methods=['GET'])
def getresult(taskid):
    client = Client('127.0.0.1','8775',admin_token='d98e80e305f381ee3df4699924d76534')
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
    client = Client('127.0.0.1','8775',admin_token='d98e80e305f381ee3df4699924d76534')
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
