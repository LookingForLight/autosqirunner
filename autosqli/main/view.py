#-*-coding:utf-8-*-
from flask import Flask, render_template, url_for, request, redirect
from .form import MyForm
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