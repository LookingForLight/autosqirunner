#coding:utf-8

import requests
import json

from utils.log import Log
class Client():

    def __init__(self,server_ip,server_root,admin_token=''):
        self.server = "http://"+server_ip+":"+server_root
        self.admin_token = admin_token
        self.headers = {'Content-Type': 'application/json'}

    def create_new_task(self):
        '''创建一个新的任务，成功返回taskid'''
        r = requests.get("{0}/task/new".format(self.server))
        taskid = r.json()['taskid']
        if taskid:
            return taskid
        else:
            return None


    def set_taskid_options(self,taskid,options):
        '''通过taskid设置url,data等'''
        option_set_api = self.server + '/option/' +taskid+ '/set'
        status = requests.post(option_set_api,json=options,headers = self.headers).json()
        if status['success']:
            Log.info('设置参数成功')
            return True

    def get_taskid_options(self,taskid):
        '''通过taskid过去配置参数'''
        option_get_api = self.server + '/option/' +taskid+ '/list'
        resp = requests.get(option_get_api).json()

        return resp


    def start_taskid_scan(self,taskid):
        '''开始扫描的方法,成功开启扫描返回True，开始扫描失败返回False'''
        scan_api = self.server + '/scan/' +taskid+ '/start'
        print("scan url:",scan_api)
        r =requests.post(scan_api,json={},headers=self.headers)
        if r.json()['success']:
            return r.json()
        else:
            return  None



    def get_taskid_status(self,taskid):
        '''获取扫描状态的方法,扫描完成返回True，正在扫描返回False'''
        scan_api = self.server + '/scan/' +taskid+ '/status'
        status = requests.get(scan_api).json()['status']
        if status=='terminated':
            return True
        elif status == 'running':
            return False
        else:
            return False



    def get_result(self,taskid):
        '''获取扫描结果的方法，存在SQL注入返回payload和注入类型等，不存在SQL注入返回空'''
        scan_result_api = self.server + '/scan/' +taskid+ '/data'
        r = requests.get(scan_result_api)
        if (r.json()['data']):
            return r.json()['data']
        else:
            return False

    def get_all_task_list(self):
        '''获取所有任务列表'''
        r = requests.get(self.server + '/admin/' + self.admin_token + "/list")
        if r.json()['success']:
            return r.json()
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
    # my = Client('10.101.52.2','8775',admin_token=' 07df5809300013183d5f9292e6e2d46e')
    my = Client('127.0.0.1','8775',admin_token='d98e80e305f381ee3df4699924d76534')


    print(my.get_taskid_options('0705f4681fc21411'))
    # print('takslist:',my.get_all_task_list())
    # options = {
    #
    #     "url":"http://127.0.0.1:8088/dvwa/vulnerabilities/sqli",
    #     "cookie":"security=low; security=low; PHPSESSID=siiu8b20e03moi6p1sdravk3co",
    #     "method":"GET",
    # }
    #
    # if my.set_task_options(options):
    #
    #     my.start_target_scan()
    #     print('扫描开始时间:',my.start_scan_time)
    #     while True:
    #         status = my.get_scan_status()
    #         if status:
    #             result = my.get_result()
    #             print('扫描结束时间:', my.end_scan_time)
    #             print(result)
    #             break
    #         else:
    #
    #             continue
