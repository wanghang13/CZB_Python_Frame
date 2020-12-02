# ******************封装请求***************
# 作者：杭仔
# *****************************************
# -*- coding:UTF-8 -*-
import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json
import datetime
import time
import requests
from Common import Get_Rand
import warnings
from Common import Read_File
from Common import Write_Excel
# from Common import Data_Transfer
from Common import Read_Config
from Common import Log
from Common import Initial
from Common import globalparam
from configobj import ConfigObj
from urllib.parse import urlencode
from urllib.parse import parse_qs, urlparse
import re
start_time = (datetime.datetime.now()+datetime.timedelta(minutes = 0.1)).strftime("%Y-%m-%d %H:%M:%S")  #获取当前时间为：活动开始时间
end_time = (datetime.datetime.now()+datetime.timedelta(minutes = 10)).strftime("%Y-%m-%d %H:%M:%S")  #获取当前时间2分钟后为：活动结束时间。minutes = 2 配置（分钟数）

# 今天日期
today = datetime.date.today()
# 昨天时间
yesterday = today - datetime.timedelta(days=1)
# 明天时间
tomorrow = today + datetime.timedelta(days=1)
acquire = today + datetime.timedelta(days=2)
# 昨天开始时间戳
yesterday_start_time = int(time.mktime(time.strptime(str(yesterday), '%Y-%m-%d')))
# 昨天结束时间戳
yesterday_end_time = int(time.mktime(time.strptime(str(today), '%Y-%m-%d'))) - 1
# 今天开始时间戳
today_start_time = yesterday_end_time + 1
# 今天结束时间戳
today_end_time = int(time.mktime(time.strptime(str(tomorrow), '%Y-%m-%d'))) - 1
# 明天开始时间戳
tomorrow_start_time = int(time.mktime(time.strptime(str(tomorrow), '%Y-%m-%d')))
# 明天结束时间戳
tomorrow_end_time = int(time.mktime(time.strptime(str(acquire), '%Y-%m-%d'))) - 1




# 结果文件路径
report_path = globalparam.report_path
# 忽略警告
warnings.filterwarnings("ignore") 

# sheet_name1 = globalparam.sheet_basic
username = globalparam.username
password = globalparam.password

class SendRequests(object):
    def __init__(self):
        self.logger = Log.TestLog()
        self.config = ConfigObj(globalparam.config_path,encoding='UTF8')
        # self.session = requests.session()

    def send_url(self, test_data):
        """
        url处理(直接拼接)
        :param test_data: excel数据
        :return: 请求url
        """
        if test_data['项目名称'] == '商户后台':
            host = self.config['RUN_API']['MP_NLSAAS']
        elif test_data['项目名称'] == '双屏机':
            host = self.config['RUN_API']['POS_OS_API']
        elif test_data['项目名称'] == 'POS机':
            host = self.config['RUN_API']['POS_API']
        elif test_data['项目名称'] == '自助机':
            host = self.config['RUN_API']['POS_SELF_API']
        url = host + test_data['url']  # 请求url
        self.logger.info("请求url: {}".format(url))
        return url

    def updaterequests(self,old_data,new_data= None,old_test_data=None):
        old_old_data = old_data
        i = 0
        try:
            old_data,new_data = eval(old_data),eval(new_data)
            if new_data !=None:
                for Dict in new_data:
                    if old_data.__contains__(Dict):
                        old_data[Dict] = new_data[Dict]
            for r in old_data:
                # print('字段名：{0}。'.format(r),end='\t')
                # print('值：{0}\t{1}。\n'.format(res[r],type(res[r])))
                # return 
                if isinstance(old_data[r], dict):
                    self.updaterequests(old_data[r],new_data)
                if isinstance(old_data[r], list) :
                    for item in old_data[r]:
                        if isinstance(item, dict) and i == 0:
                            if isinstance(item, dict):
                                self.updaterequests(item,new_data)
                            i += 1
                        else:
                            break 
            return str(old_data)
        except Exception as e:
            self.logger.error("错误信息：{}".format(e))
            return str(old_old_data)

    def updaterequests2(self,old_data,field= None):
        i=0
        try:
            for r in old_data:
                if r == field:
                    # print('pass')
                    # print(old_data[r])
                    self.data = old_data[r]
                    break
                if isinstance(old_data[r], dict):
                    self.updaterequests2(old_data[r],field)
                if isinstance(old_data[r], list) :
                    for item in old_data[r]:
                        if isinstance(item, dict) and i == 0:
                            if isinstance(item, dict):
                                self.updaterequests2(item,field)
                            i += 1
                        else:
                            break
            return str(self.data)
        except Exception as e:
            self.logger.error("错误信息：{}".format(e))
            return str(self.data)

    def chenckassociateid(self,test_data,old_test_data=None):
        t_data = eval(test_data['associateid'])
        line = eval(t_data['associateid'])
        oldassociatefield = t_data['associatefield']
        old_test_data1 = old_test_data[line-1]
        session = requests.session()
        res = self.send_requests(session,old_test_data1)
        data = eval(test_data['data'])
        test_data['data']= data
        associatefield_test = oldassociatefield.split(",")
        for associatefield in associatefield_test:
            if associatefield in 'token':
                List = []
                res_data = self.updaterequests2(res,associatefield)
                test_data['data']['merchant_type'] = self.updaterequests2(res,'merchant_type')
                test_data['data']['merchant_id'] = self.updaterequests2(res,'merchant_id')
                test_data['data']['merchant_name'] = self.updaterequests2(res,'merchant_name')
                List.append(self.updaterequests2(res,'merchant_id'))
                test_data['data']['arr_merchant_ids'] = List
                test_data['data'][associatefield] = res_data
            elif associatefield in 'None':
                pass
            else:
                res_data = self.updaterequests2(res,associatefield)
                test_data['data'][associatefield] = res_data
        return str(test_data['data'])



    def chencktestdata(self,test_data,old_test_data=None):
        if test_data['associateid']!='' and test_data['associateid'] !=None and old_test_data != None:
            test_data['data'] = self.chenckassociateid(test_data,old_test_data)
        else:
            self.logger.info("************   Excel 中的 associateid 字段 为空。不做接口关联处理。  *******************")
        if test_data['updatadict']:
            test_data['data'] = self.updaterequests(test_data['data'],test_data['updatadict'])
        else:
            self.logger.info("************   Excel 中的 updatadict 字段 为空。不做data数据更新处理。   *******************") 
        if  test_data['timedata']:
            if test_data['timedata'] == '默认':
                data = eval(test_data['data'])
                data['start_time'] = start_time
                data['end_time'] = end_time
                test_data['data'] = str(data)
            elif test_data['timedata'] == 'start>end':
                data = eval(test_data['data'])
                data['start_time'] = start_time
                data['end_time'] = (datetime.datetime.now()+datetime.timedelta(minutes = -1)).strftime("%Y-%m-%d %H:%M:%S")
                test_data['data'] = str(data)
            elif test_data['timedata'] == 'start=end':
                data = eval(test_data['data'])
                data['start_time'] = start_time
                data['end_time'] = start_time
                test_data['data'] = str(data)
        else:
            self.logger.info("************   Excel 中的 timedata 字段 为空。不做时间字段更新处理。   *******************") 
        return test_data


    def send_requests(self, session, test_data,old_test_data=None, param=None):
        """
        请求
        :param session: session消息
        :param test_data: 测试数据
        :param sheet: 用例页名称
        :param param:初始化数据
        :return: 测试结果
        """
        # print(old_test_data)
        # quit()
        test_data = self.chencktestdata(test_data,old_test_data)

        method = test_data["method"]  # 请求方式
        self.logger.info("请求方式：{}".format(method))
        results = {}  # 接受返回数据
        url = self.send_url(test_data)
        body = test_data['data']
        # params_data = '?' + params
        # query = urlparse(params_data).query
        # if test_data['params'] != '' and test_data['params'] != None:
        params = parse_qs(urlparse('?' + test_data['params']).query)
        # print(params)
        headers = test_data['headers']
        # 发送请求
        try:
            if test_data['项目名称'] == 'POS机':
                if test_data['url'] == '/login/userLogin':
                    r = requests.post(url = url, data = params,headers=eval(headers))
                    self.config['POS_API_INI']['TOKEN'] = r.json()['data']['token']
                    self.config['POS_API_INI']['MERCHANT_TYPE'] = r.json()['data']['merchant_type']
                    self.config['POS_API_INI']['MERCHANT_ID'] = r.json()['data']['st_id']
                    self.config['POS_API_INI']['U_ID'] = r.json()['data']['u_id']
                    self.config.write()
                else:
                    if method.upper() == 'POST':
                        
                        params['token'] = self.config['POS_API_INI']['TOKEN']
                        params['user_id'] = self.config['POS_API_INI']['U_ID']
                        test_params = eval(params['data'][0])
                        test_params['st_id'] = self.config['POS_API_INI']['MERCHANT_ID']
                        test_params['st_type'] = self.config['POS_API_INI']['MERCHANT_TYPE']
                        # test_params['gun_id'] = self.config['POS_API_INI']['GUN_ID']
                        if test_data['标题'] == '零管-输入金额-现金支付':
                            test_params['gun_id'] = self.config['POS_API_INI']['RETAIL_GUN_ID']
                            test_params['oil_name'] = self.config['POS_API_INI']['RETAIL_ENERGY_NAME']
                            test_params['gun_number'] = self.config['POS_API_INI']['RETAIL_GUN']
                            test_params['energy_number'] = self.config['POS_API_INI']['RETAIL_ENERGY_NUMBER']
                            test_params['energy_type'] = self.config['POS_API_INI']['RETAIL_ENERGY_TYPE']
                            test_params['id'] = self.config['POS_API_INI']['RETAIL_GUN_ID']
                            test_params['oil_id'] = self.config['POS_API_INI']['RETAIL_OIL_ID']
                        elif test_data['标题'] == '非零管-输入金额-现金支付':
                            test_params['gun_id'] = self.config['POS_API_INI']['STATIC_GUN_ID']
                            test_params['oil_name'] = self.config['POS_API_INI']['STATIC_ENERGY_NAME']
                            test_params['gun_number'] = self.config['POS_API_INI']['STATIC_GUN']
                            test_params['energy_number'] = self.config['POS_API_INI']['STATIC_ENERGY_NUMBER']
                            test_params['energy_type'] = self.config['POS_API_INI']['STATIC_ENERGY_TYPE']
                            test_params['id'] = self.config['POS_API_INI']['STATIC_GUN_ID']
                            test_params['oil_id'] = self.config['POS_API_INI']['STATIC_OIL_ID']
                        params['data'] =json.dumps(test_params)
                        r = requests.post(url = url, data = params,headers=eval(headers))

                    elif method.upper() == 'GET':
                        pass

            elif test_data['项目名称'] == '双屏机': 
                if test_data['url'] == '/user/login':
                    r = requests.post(url = url, data = json.dumps(eval(body)),headers = {'Content-Type': 'application/json'})
                    Dict = {'Content-Type': 'application/json;charset=utf-8'}
                    Dict['token'] = r.json()['data']['token']
                    Dict['aid'] = r.json()['data']['id']
                    self.config['POS_OS_API_INI']['HEADERS'] = str(Dict)
                    self.config['POS_OS_API_INI']['MERCHANT_TYPE'] = r.json()['data']['merchant_info']['merchant_type']
                    self.config['POS_OS_API_INI']['MERCHANT_ID'] = r.json()['data']['merchant_info']['merchant_id']
                    headers = Dict
                else :
                    if method.upper() == 'POST':
                        body = eval(body)
                        body['merchant_type'] = self.config['POS_OS_API_INI']['MERCHANT_TYPE']
                        body['merchant_id'] = self.config['POS_OS_API_INI']['MERCHANT_ID']
                        headers = eval(self.config['POS_OS_API_INI']['HEADERS'])
                        # if test_data['url'] == '/order/abandon'or test_data['url'] == '/order/quickpass/pay':
                        if test_data['url'] == '/order/abandon':
                            body['order_id'] = self.config['POS_OS_API_INI']['ORDER_BOX_ID']
                            headers['password'] = self.config['POS_OS_API_INI']['PASSWORD']
                        else :
                            body['order_id'] = [self.config['POS_OS_API_INI']['ORDER_BOX_ID']]

                        # if test_data['url'] == '/order/refund' or test_data['url'] == '/order/quickpass/pay':
                        if test_data['url'] == '/order/refund':
                            body['order_code'] = self.config['POS_OS_API_INI']['REFUND_ORDER_CODE']
                        elif test_data['url'] == '/order/abandon' :
                            pass
                        else:
                            body['order_code'] = [self.config['POS_OS_API_INI']['REFUND_ORDER_CODE']]
                        if test_data['url'] == '/recharge/top_up_order' or test_data['url'] == '/recharge/top_up':
                            body['user_id'] = self.config['POS_OS_API_INI']['USER_ID']
                            body['card_code'] = self.config['POS_OS_API_INI']['CARD_CODE']
                            body['card_id'] = self.config['POS_OS_API_INI']['CARD_ID']
                            body['user_card_code'] = self.config['POS_OS_API_INI']['CARD_CODE']
                            if test_data['url'] != '/order/batch/pay':
                                body['order_code'] = self.config['POS_OS_API_INI']['ORDER_CODE']
                        self.config.write()
                        
                        
                        if type(body) == type(''):
                            body = eval(body)

                        r = requests.post(url = url, data = json.dumps(body) ,headers = headers)

                        if test_data['url'] == '/order/quickpass/pay':
                            pass
                        if test_data['url'] == '/recharge/top_up_order':
                            self.config['POS_OS_API_INI']['ORDER_CODE'] = r.json()['data']['order_code']
                        if test_data['url'] == '/order/pay':
                            time.sleep(0.85)
                    elif method.upper() == 'GET':
                        params['merchant_type'] = self.config['POS_OS_API_INI']['MERCHANT_TYPE']
                        params['merchant_id'] = self.config['POS_OS_API_INI']['MERCHANT_ID']
                        if test_data['url'] == '/orders':
                            params['begin_time'] = [str(today_start_time)]
                            params['end_time'] = [str(today_end_time)]
                        headers = self.config['POS_OS_API_INI']['HEADERS']
                        if test_data['url'] == '/recharge/user_card_list':
                            params['user_id'] = self.config['POS_OS_API_INI']['USER_ID']
                            params['phone'] = self.config['POS_OS_API_INI']['MOBILE']
                        r = requests.get(url = url , params = params,headers = eval(headers))
                        if test_data['url'] == '/order/gun_list':
                            self.config['POS_OS_API_INI']['ORDER_BOX_ID'] = str(r.json()['data'][0]['list'][0]['id'])
                        elif test_data['url'] == '/orders':
                            self.config['POS_OS_API_INI']['REFUND_ORDER_CODE'] = str(r.json()['data'][0]['order_code'])
                        elif test_data['url'] == '/client/detail':
                            self.config['POS_OS_API_INI']['USER_ID'] = str(r.json()['data']['user_id'])
                            self.config['POS_OS_API_INI']['MOBILE'] = str(r.json()['data']['mobile'])
                        elif test_data['url'] == '/recharge/user_card_list':
                            self.config['POS_OS_API_INI']['CARD_CODE'] = str(r.json()['data'][0]['user_card']['code'])
                            self.config['POS_OS_API_INI']['CARD_ID'] = str(r.json()['data'][0]['user_card']['card_id'])
            elif test_data['项目名称'] == '自助机':
                pass

            elif test_data['项目名称'] == '商户后台':
                body = eval(body)
                if test_data['url'] != '/api/user/Login/login_admin':
                    body['token'] = self.config['MP_NLSAAS_API_INI']['TOKEN']
                    body['merchant_id'] = self.config['MP_NLSAAS_API_INI']['MERCHANT_ID']
                    body['arr_merchant_ids'] = [self.config['MP_NLSAAS_API_INI']['MERCHANT_ID']]
                    # body['uid'] = self.config['MP_NLSAAS_API_INI']['USERID']
                if test_data['url'] == '/api/coupon/coupons/create_coupons':
                    body['coupon_start_time'] = start_time
                    body['coupon_end_time'] = end_time
                    body['amount_rule'][0]['product_id'] = self.config['MP_NLSAAS_API_INI']['ENERGY_ID_LIST']
                elif test_data['url'] == '/api/activities/send-gift-with-purchase-activity/create':
                    body['activity_rule'][0]['step_award'][0]['arr_coupon_id_amount'][0] = self.config['MP_NLSAAS_API_INI']['COUPON_ID']
                elif test_data['url'] == '/api/coupon/coupons/activation_coupon':
                    body['coupon_id'] = self.config['MP_NLSAAS_API_INI']['COUPON_ID']
                elif test_data['url'] == '/api/activity/red_pack/create':
                    body['award'][0]['value'][0]['id'] = self.config['MP_NLSAAS_API_INI']['COUPON_ID']
                    body['station_range'] = self.config['MP_NLSAAS_API_INI']['MERCHANT_ID']
                elif test_data['url'] == '/activities/recharge_send_coupon_activity/create':
                    body['activity_rule'][0]['recharge_award'][0]['id'] = self.config['MP_NLSAAS_API_INI']['COUPON_ID']
                r = session.request(method=method,
                                    url=url,
                                    params=params,
                                    headers=eval(headers),
                                    data=json.dumps(body),
                                    verify=True
                                    )
                if test_data['url'] == '/api/user/Login/login_admin':
                    self.config['MP_NLSAAS_API_INI']['TOKEN'] = r.json()['data']['token']
                    self.config['MP_NLSAAS_API_INI']['MERCHANT_ID'] = r.json()['data']['contract']['confirm_merchant_ids'][0]
                    # self.config['MP_NLSAAS_API_INI']['MERCHANT_ID'] = r.json['data']['contract']['confirm_merchant_ids'][0]
                    # self.config['MP_NLSAAS_API_INI']['USERID'] = r.json['data']['id']
                elif test_data['url'] == '/api/coupon/coupons/create_coupons':
                    self.config['MP_NLSAAS_API_INI']['COUPON_ID'] = r.json()['data']['coupon_id']
                elif test_data['url'] == '/api/energy/energy/get_energy_price_list':
                    energy_id_list = []
                    for List in r.json()['data']:
                        energy_id_list.append(List['energy_id'])
                        self.config['MP_NLSAAS_API_INI']['ENERGY_ID_LIST'] = energy_id_list
                elif test_data['url'] == '/api/energy/energy/get_gun_list':
                    for gun_oil_arr in r.json()['data']:
                        if gun_oil_arr['retail_status'] == 2:
                            self.config['POS_API_INI']['STATIC_GUN'] = gun_oil_arr['gun_number']
                            self.config['POS_API_INI']['STATIC_ENERGY_NAME'] = gun_oil_arr['energy_name']
                            self.config['POS_API_INI']['STATIC_GUN_NUM'] = gun_oil_arr['gun_number']
                            self.config['POS_API_INI']['STATIC_GUN_ID'] = gun_oil_arr['id']
                            self.config['POS_API_INI']['STATIC_OIL_ID'] = gun_oil_arr['energy_id']
                            self.config['POS_API_INI']['STATIC_ENERGY_TYPE'] = gun_oil_arr['energy_type']
                            self.config['POS_API_INI']['STATIC_ENERGY_NUMBER'] = gun_oil_arr['energy_number']
                            break
                    for gun_oil_arr in r.json()['data']:
                        if gun_oil_arr['retail_status'] == 1:
                            self.config['POS_API_INI']['RETAIL_GUN'] = gun_oil_arr['gun_number']
                            self.config['POS_API_INI']['RETAIL_ENERGY_NAME'] = gun_oil_arr['energy_name']
                            self.config['POS_API_INI']['RETAIL_GUN_NUM'] = gun_oil_arr['gun_number']
                            self.config['POS_API_INI']['RETAIL_GUN_ID'] = gun_oil_arr['id']
                            self.config['POS_API_INI']['RETAIL_OIL_ID'] = gun_oil_arr['energy_id']
                            self.config['POS_API_INI']['RETAIL_ENERGY_TYPE'] = gun_oil_arr['energy_type']
                            self.config['POS_API_INI']['RETAIL_ENERGY_NUMBER'] = gun_oil_arr['energy_number']
                            break
                            
            # print(r.json())
            # 保存请求结果
            self.config.write()
            results['id'] = test_data['id']
            results["body"] = body
            results['rowNum'] = test_data['rowNum']
            results["text"] = r.content.decode("utf-8")
            results["status_code"] = str(r.status_code)  # 状态码转成str
            if results["status_code"] != "200":
                self.logger.error("请求错误！接口返回状态：%s" % r.status_code)
                results["error"] = results["text"]
            else:
                results["error"] = ""
            results["json"] = r.json()
            results["json_status"] = r.json()['status']
            results["times"] = "%.3f" % (r.elapsed.total_seconds())  # 接口请求时间保留3位小数
            self.logger.info("请求参数：{}".format(body))
            self.logger.info("请求params：{}".format(params))
            self.logger.info("请求headers：{}".format(headers))
            self.logger.info("检查点->：%s" % test_data["checkstatus"])
            if test_data["checkstatus"] == str(r.json()['status']):
                results["result"], results["msg"] = "pass", ""
                # if test_data['url'] != '/order/gun_list' or test_data['url'] != '/api/user/Login/login_admin':
                if test_data['url'].find('list') >=0 or test_data['url'].find('List') >=0 or test_data['url'].find('login') >=0 or test_data['url'].find('Login') >=0 :
                    pass
                else:
                    pass
                    self.logger.info("用例执行成功！页面返回信息：%s" % r.json())
            else:
                results["result"], results["msg"] = "fail", r.content
                self.logger.error("用例执行失败！页面返回信息：{}".format(r.json()))
            self.logger.info("用例测试结果:   %s---->   %s" % (test_data['id'], results["result"]))
            self.logger.info("*******执行用例完成：-----  %s  ----**********\n" % test_data['id'])
            return results

        except Exception as msg:
            self.logger.error("用例执行错误！错误信息：{}".format(msg))
            self.logger.info("用例测试结果:   %s---->   %s" % (test_data['id'], results["result"]))
            self.logger.info("*******执行用例完成：-----  %s  ----**********" % test_data['id'])
            results["result"], results["msg"] = "fail", "请求错误！请检查参数设置！"
            results['error'], results['times'] = "", ""
        return results


    def send_requests2(self, session, test_data, param=None):
        """
        请求
        :param session: session消息
        :param test_data: 测试数据
        :param sheet: 用例页名称
        :param param:初始化数据
        :return: 测试结果
        """
        # print('111111111111111111111111111\n',test_data)
        # test_data = self.chencktestdata(test_data)
        method = test_data["method"]  # 请求方式
        self.logger.info("请求方式：{}".format(method))
        # results = {}  # 接受返回数据
        url = self.send_url(test_data)
        body, params = test_data['data'], test_data['params']
        headers = test_data['headers']
        # 发送请求
        try:
            r = session.request(method=method,
                                url=url,
                                params=params,
                                headers=eval(headers),
                                data=json.dumps(eval(body)),
                                verify=True
                                )
            # print(r.json()['data']['token'],'``````````````asdfjoisadfjlasdjfiosadjfo`````````````````')
            # 保存请求结果
            if str(r.status_code) != "200":
                self.logger.error("请求错误！接口返回状态：%s" % r.status_code)
            self.logger.info("请求参数：{}".format(body))
            self.logger.info("检查点->：%s" % test_data["checkstatus"])
            if test_data["checkstatus"] == str(r.json()['status']):
                # self.logger.info("用例执行成功！页面返回信息：%s" % r.json()['status'])
                self.logger.info("用例执行成功！页面返回信息：%s" % r.json()['status'])
            else:
                self.logger.error("用例执行失败！页面返回信息：{}".format(r.json()['info']))
            self.logger.info("*******执行用例完成：-----  %s  ----**********\n" % test_data['id'])
            # print('------------------------------------------')
            return r.json()
        except Exception as msg:
            self.logger.error("用例执行错误！错误信息：{}".format(msg))
            self.logger.info("*******执行用例完成：-----  %s  ----**********" % test_data['id'])
        return r.json()

    # 测试结果写入excel
    def wirte_result(self, result, filename=report_path, sheet="Sheet1"):
        """
        测试结果写入excel
        :param result: 测试结果（字典格式）
        :param filename: excel路径（到文件）
        :param sheet: sheet名称
        :return:无
        """
        num = 14  # 开始写入的列数
        try:
            # 返回结果的行数row_nub
            row_nub = result['rowNum'] + 2
            # 调用写入函数（默认写入Sheet1）
            wt = Write_Excel.WriteExcel(filename, sheet)
            if result['result'] == "fail":
                wt.write(row_nub, num + 4, result['result'], colour='red')  # 测试结果 pass 还是fail
                wt.write(row_nub, num + 3, result['msg'], colour='red')  # 返回信息
            elif result['result'] == "pass":
                wt.write(row_nub, num + 4, result['result'], colour='green')  # 测试结果 pass 还是fail
                wt.write(row_nub, num + 3, result['msg'], colour='green') 
            if result['status_code'] == '200':
                wt.write(row_nub, num + 2, result['status_code'], colour='green')  # 写入返回状态码statuscode
                # wt.write(row_nub, num + 2, result['error'])  # 状态码非200时的返回信息
                wt.write(row_nub, num, str(result['json']),colour='black')  # 写入json信息
                # wt.write(row_nub, num - 6, str(result['body']),colour='black')  # 写入json信息
            elif result['json_status'] != '200':
                wt.write(row_nub, num + 2, result['status_code'], colour='red')  # 写入返回状态码statuscode
                wt.write(row_nub, num, str(result['json']),colour='red')  # 写入json信息
            else:
                wt.write(row_nub, num + 2, result['status_code'], colour='red')  # 写入返回状态码statuscode
                wt.write(row_nub, num, str(result['json']),colour='red')  # 写入json信息
                # wt.write(row_nub, num + 2, result['error'], colour='red')  # 状态码非200时的返回信息
            if float(result['times']) > 1:
                wt.write(row_nub, num + 1, result['times'], colour='red')  # 耗时
            else:
                wt.write(row_nub, num + 1, result['times'], colour='green')  # 耗时
        except Exception as e:
            self.logger.error("写入结果失败！结果的行数{},报错信息:{}".format(result['rowNum'], e))
        


# if __name__ == "__main__":
#     username = globalparam.username
#     password = globalparam.password
#     sheet_name = 'Sheet2'
#     father_path = globalparam.data_path  # 当前文件目录的父级目录
#     excelPath = os.path.join(father_path,"Test_Case.xlsx")
#     data = Read_File.ExcelUtil(excelPath, sheet_name=sheet_name).dict_data()
#     s = requests.session()
#     # 用例id
#     i = 2
#     for data in data :
#         res = SendRequests().send_requests(s, data, sheet_name)
