#coding:utf-8

import requests
import json
from datetime import datetime

class Client():

    def __init__(self,server_ip,server_root,admin_token='',taskid='',filepath=None):
        self.server = "http://"+server_ip+":"+server_root
        self.admin_token = admin_token
        self.taskid = taskid
        self.filepath = ""
        self.status = ""
        self.start_scan_time = ""
        self.end_scan_time = ""
        self.engineid=""
        self.headers = {'Content-Type': 'application/json'}

    def create_new_task(self):
        '''创建一个新的任务，成功返回taskid'''
        r = requests.get("{0}/task/new".format(self.server))
        self.taskid = r.json()['taskid']
        if self.taskid != "":
            return self.taskid
        else:
            return None

    def set_task_options(self,options):
        '''设置任务扫描的url,data等'''
        option_set_api = self.server + '/option/' +self.taskid+ '/set'
        status = requests.post(option_set_api,json=options,headers = self.headers).json()
        if status['success']:
            print("设置配置文件成功")


    def start_target_scan(self):
        '''开始扫描的方法,成功开启扫描返回True，开始扫描失败返回False'''
        scan_api = self.server + '/scan/' +self.taskid+ '/start'
        print(self.filepath)
        r =requests.post(scan_api,json={},headers=self.headers)
        print(r.text)
        if r.json()['success']:
            self.start_scan_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return r.json()['engineid']
        else:
            return  None

    def get_scan_status(self):
        '''获取扫描状态的方法,扫描完成返回True，正在扫描返回False'''
        scan_api = self.server + '/scan/' +self.taskid+ '/status'
        self.status = requests.get(scan_api).json()['status']
        if self.status=='terminated':
            self.end_scan_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return True
        elif self.status == 'running':
            return False
        else:
            self.status = False

    def get_result(self):
        '''获取扫描结果的方法，存在SQL注入返回payload和注入类型等，不存在SQL注入返回空'''
        scan_result_api = self.server + '/scan/' +self.taskid+ '/data'
        if (self.status):
             r = requests.get(scan_result_api)
             if (r.json()['data']):
                 return r.json()['data']
             else:
                 return None

    def get_all_task_list(self):
        '''获取所有任务列表'''
        r = requests.get(self.server + '/admin/' + self.admin_token + "/list")
        if r.json()['success']:
            #print(r.json()['tasks'])
            return r.json()['tasks']
        else:
            return None

    def del_a_task(self,taskid):
        '''删除一个任务'''
        r = requests.get(self.server + '/task/' + taskid + '/delete')
        if r.json()['success']:
            return True
        else:
            return False

    def stop_a_scan(self,taskid):
        '''停止一个扫描任务'''
        r = requests.get(self.server + '/scan/' + taskid + '/stop')
        if r.json()['success']:
            return True
        else:
            return False

    def flush_all_tasks(self):
        '''清空所有任务'''
        r =requests.get(self.server + '/admin/' + self.admin_token + "/flush")
        if r.json()['success']:
            return True
        else:
            return False

    def get_scan_log(self,taskid):
        '''获取log'''
        r = requests.get(self.server + '/scan/' + taskid + '/log')
        return r.json()

if __name__ == '__main__':
    my = Client('10.101.52.2','8775',admin_token='710092afc952231b8ab984691aec1a0e')
    # print "taskid:",my.create_new_task()
    # options = {
    #
    #     "url":"http://127.0.0.1:8088/dvwa/vulnerabilities/sqli?id=2&Submit=Submit",
    #     "cookie":"security=low; security=low; PHPSESSID=s64i0e40hio3lhvcn7i9u9pv58"
    # }
    # my.set_task_options(options)
    # my.start_target_scan()
    # while True:
    #     status = my.get_scan_status()
    #     if status:
    #         result = my.get_result()
    #
    #         print result
    #         break
    #     else:
    #         continue
