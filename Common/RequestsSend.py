# ******************封装请求***************
# 作者：杭仔
# *****************************************
# -*- coding:UTF-8 -*-
import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json
import datetime
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
import re
start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")                                          #获取当前时间为：活动开始时间
start_time = (datetime.datetime.now()+datetime.timedelta(minutes = 0.1)).strftime("%Y-%m-%d %H:%M:%S")  #获取当前时间为：活动开始时间
end_time = (datetime.datetime.now()+datetime.timedelta(minutes = 10)).strftime("%Y-%m-%d %H:%M:%S")  #获取当前时间2分钟后为：活动结束时间。minutes = 2 配置（分钟数）
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
        # self.session = requests.session()

    def send_url(self, test_data):
        """
        url处理(直接拼接)
        :param test_data: excel数据
        :return: 请求url
        """
        # url = test_data['url'] +test_data['api']  # 请求url
        url = test_data['url']  # 请求url
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
        res = self.send_requests2(session,old_test_data1)
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
        body, params = test_data['data'], test_data['params']
        headers = test_data['headers']
        # 发送请求
        try:
            r = session.request(method=method,
                                url=url,
                                params=params,
                                headers=eval(headers),
                                data=json.dumps(eval(body)),
                                verify=False
                                )
            # print(r.json())
            # 保存请求结果
            results['id'] = test_data['id']
            results['rowNum'] = test_data['rowNum']
            results["text"] = r.content.decode("utf-8")
            results["status_code"] = str(r.status_code)  # 状态码转成str
            if results["status_code"] != "200":
                self.logger.error("请求错误！接口返回状态：%s" % r.status_code)
                results["error"] = results["text"]
            else:
                results["error"] = ""
            results["json"] = r.json()
            results["times"] = "%.3f" % (r.elapsed.total_seconds())  # 接口请求时间保留3位小数
            self.logger.info("请求参数：{}".format(body))
            self.logger.info("检查点->：%s" % test_data["checkstatus"])
            if test_data["checkstatus"] == str(r.json()['status']):
                results["result"], results["msg"] = "pass", ""
                # self.logger.info("用例执行成功！页面返回信息：%s" % r.json()['status'])
                self.logger.info("用例执行成功！页面返回信息：%s" % r.json())
            else:
                results["result"], results["msg"] = "fail", r.content.decode("utf-8")
                self.logger.error("用例执行失败！页面返回信息：{}".format(r.json()))
            self.logger.info("用例测试结果:   %s---->   %s" % (test_data['id'], results["result"]))
            self.logger.info("*******执行用例完成：-----  %s  ----**********\n" % test_data['id'])
            return results

        except Exception as msg:
            self.logger.error("用例执行错误！错误信息：{}".format(msg))
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
                                verify=False
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
        num = 19  # 开始写入的列数
        try:
            # 返回结果的行数row_nub
            row_nub = result['rowNum']
            # 调用写入函数（默认写入Sheet1）
            wt = Write_Excel.WriteExcel(filename, sheet)
            if result['result'] == "fail":
                wt.write(row_nub, num + 3, result['result'], colour='red')  # 测试结果 pass 还是fail
                wt.write(row_nub, num + 4, result['msg'], colour='red')  # 返回信息
            else:
                wt.write(row_nub, num + 3, result['result'], colour='green')  # 测试结果 pass 还是fail
                wt.write(row_nub, num + 4, result['msg'])  # 错误信息
            if result['status_code'] == '200':
                wt.write(row_nub, num, result['status_code'], colour='green')  # 写入返回状态码statuscode
                wt.write(row_nub, num + 2, result['error'])  # 状态码非200时的返回信息
            else:
                wt.write(row_nub, num, result['status_code'], colour='red')  # 写入返回状态码statuscode
                wt.write(row_nub, num + 2, result['error'], colour='red')  # 状态码非200时的返回信息
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
