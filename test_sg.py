

from Common.Read_File import ExcelUtil
from Common import globalparam
from Common.Log import TestLog
import requests
import os
import json

def HTTP_Requests(url,method,data,headers=''):
    if method.upper() == 'GET':
        print('还没写。')
        # res = requests.get(url = url,method = method,data = data)
        pass
    elif method.upper() == 'POST':
        # print(url)
        res = requests.post(url = url,data = json.dumps(data),headers = eval(headers))
        return res


excel_path = os.path.join(globalparam.data_path,'日常冒烟测试点.xlsx')
data = ExcelUtil(excel_path,'商户后台接口冒烟3').dict_data()
for i in data:
    # print('第{}条用例.请求方式为:{}'.format(i['id'],i['method']))
    # print('请求参数：{}'.format(i['data']))
    TestLog().info('第{}条用例.请求方式为:{}'.format(i['id'],i['method']))
    TestLog().info('请求参数：{}'.format(i['data']))

    url = 'https://mp.nlsaas.com' + i['url']
    res = HTTP_Requests(url,i['method'],eval(i['data']),i['headers'])

    if str(res.json()['status']) == i['checkstatus']:
        TestLog().info('接口case 测试通过！PASS')
    else:
        TestLog().info('接口case 测试不通过！FAIL')


    # print(res.json())
    # print()