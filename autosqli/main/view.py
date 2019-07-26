#-*-coding:utf-8-*-
from flask import Flask, render_template, url_for, request, redirect,abort,jsonify
from .form import MyForm,AutosqliForm
from . import sqil
from ..core.autosqli import Client

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


@sqil.route('/home2',methods=['GET'])
def home():

    if request.method == 'GET':
        return render_template('autosqli/bootvue.html')


@sqil.route('/recordlist',methods=['GET'])
def recordlist():


    client = Client('10.101.52.2','8775',admin_token=' 8aee6e49c56499637ae2d6f6e6733445')
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

