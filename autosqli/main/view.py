#-*-coding:utf-8-*-
from flask import Flask, render_template, url_for, request, redirect
from .form import MyForm,AutosqliForm
from . import sqil

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
