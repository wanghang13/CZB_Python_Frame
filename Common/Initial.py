# ****************初始化*****************
# 作者：杭仔
# *****************************************
# -*- coding:UTF-8 -*-
import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import requests
from Common import Log
import warnings

# 忽略警告
warnings.filterwarnings("ignore")


class Initials(object):
    def __init__(self):
        self.logger = Log.TestLog()
    def get_token(self, user_name, pass_word):
        params = {}
        try:
            url = "http://106.52.206.103:30020/api/user/Login/login_admin"
            data = {"admin_name":user_name,"password":pass_word,"admin_type":2,"login_type":1,"token":""}
            headers = {'Content-Type': 'application/json;charset=UTF-8'}
            response = requests.post(url, json=data, headers=headers)
            params['token'] = response.json()['data']['token']
            if len(params) == 0:
                self.logger.error("获取token值失败！")
            else: 
                self.logger.info('接口地址：{}'.format(url))
                self.logger.info('接口请求：{}'.format(data))
                self.logger.info('获取Token：{}'.format(params))
                # self.logger.info('接口返回：{}'.format(response.json()))
            return params
        except Exception as e:
            self.logger.error("基础后台登录失败!错误信息:{}".format(e))
            # return '未获取到token。'


if __name__ == "__main__":
    
    import globalparam
    print(Initials().get_token(globalparam.username, globalparam.password))