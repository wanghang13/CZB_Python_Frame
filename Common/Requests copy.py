# ******************封装请求***************
# 作者：杭仔
# *****************************************
# -*- coding:UTF-8 -*-
import json
import os
import requests
# from Common.Get_Rand import Getrand
import Get_Rand
import warnings
from Common.Read_File import ExcelUtil
from Common.Write_Excel import WriteExcel
# from Common import Data_Transfer
from Common.Read_Config import ReadConfig
import Read_Config
import Log
from Common.Initial import Initial
import globalparam
import re

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

    def data_findall(self, data_body, fields, nember=0):
        """
        替换参数
        data_body:str
        fields:dist(通过接口或者sql返回)
        注意：调用时test_data要转成str
        {"keyword": "****"}
        {"state": "****"}
        """
        new_data = data_body
        try:
            keys = list(fields.keys())  # 获取要更新的字段
            value = list(fields.values())  # 获取要更新的字段的值
            for a in range(len(keys)):
                test_str = re.findall(r"'" + str(keys[a]) + "': '.*?'", str(data_body))  # 提取要更新的字符串
                if type(value[a]) is str:
                    test_findall = "'" + keys[a] + "'" + ": " + "'" + value[a] + "'"  # 拼接要更新的字符串（str型）
                else:
                    test_findall = "'" + keys[a] + "'" + ": " + str(value[a])  # 拼接要更新的字符串 (int型)
                if len(test_str) < 1:
                    self.logger.error("获取参数失败！请检查参数！")
                # new_data = re.sub(test_str[nember], test_findall, str(data_body))  # 替换字符串
                new_data = str(new_data).replace(test_str[nember], test_findall)  # 替换字符串
            return new_data
        except Exception:
            self.logger.error("参数替换错误！")
            raise

    def send_url(self, test_data):
        """
        url处理(直接拼接)
        :param test_data: excel数据
        :return: 请求url
        """
        url = test_data['url']  # 请求url
        self.logger.info("请求url: {}".format(url))
        return url

    def send_url2(self, sheet, test_data):
        pass
        """
        url处理（替换url参数）
        :param sheet: 用例sheet页名称
        :param test_data: 测试数据
        :return: 请求url
        """
        self.logger.info("---------开始更新请求参数！---------")
        try:
            if test_data["transfer"] != '':
                self.logger.info("------开始获取关联接口参数！------")
                data1 = Data_Transfer.DataTransfer().transfer_boyd(sheet, **test_data)
                for j in range(len(eval(test_data["field"]))):
                    value = eval(test_data["field"])[j]
                    url_join = str(data1[value[0]])
                    # 替换url参数
                    test_data["url"] = test_data["url"].replace('{' + value[0] + '}', url_join)
                self.logger.info("------获取关联接口参数完成！------")
            # 获取SQL查询参数
            if test_data["sql"] != '':
                self.logger.info("------开始获取SQL查询参数!------")
                data2 = MysqlTest().mysql_1(**test_data)
                # 多个替换
                for j in range(len(eval(test_data["sqlfield"]))):
                    value = eval(test_data["sqlfield"])[j]
                    url_join = str(data2[value[0]])
                    # 替换url参数
                    test_data["url"] = test_data["url"].replace('{' + value[0] + '}', url_join)
                self.logger.info("------获取SQL查询参数完成!------")
        except Exception:
            raise
        self.logger.info("------数据更新完成，继续执行当前用例！------")
        # 拼接url
        url = self.send_url(test_data)
        return url

    def send_headers(self, test_data):
        """
        请求头处理
        :param test_data: 测试数据
        :return: 请求头
        """
        header = {'Content-Type': 'application/json;charset=UTF-8',
                  'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 ' +
                                '(KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
                  }
        if len(test_data['headers']) > 0:
            header.update(eval(test_data['headers']))
        if test_data["接口名称"] != "登录":
            header = dict(header, **Initial().get_token(username, password))
        self.logger.info("请求头部：%s" % header)
        return header

    def send_body_data(self, sheet, test_data, param=None):
        pass
        """
        请求参数处理（body、param）
        :param sheet: 用例页名称
        :param test_data: 测试数据
        :param param: 初始化数据
        :return: 请求参数（body、param）
        """
        # 获取关联接口参数
        self.logger.info("---------开始更新请求参数！---------")
        if test_data["transfer"] != '':
            self.logger.info("------开始获取关联接口参数！------")
            data1 = Data_Transfer.DataTransfer().transfer_boyd(sheet, **test_data)
            self.logger.info("------获取关联接口参数完成！------")
        else:
            data1 = {}
        # 获取SQL查询参数
        if test_data["sql"] != '':
            self.logger.info("------开始获取SQL查询参数!------")
            data2 = MysqlTest().mysql_1(**test_data)
            self.logger.info("------获取SQL查询参数完成!------")
        else:
            data2 = {}
        self.logger.info("------数据更新完成，继续执行当前用例！------")
        # 合并Body参数
        try:
            param2 = param
            param3 = dict(data1, **data2)
            # 更新body参数
            if (test_data["transfer"] != '' or test_data["sql"] != '') and test_data["body"] != '' and \
                    test_data["params"] == '':
                params = param2
                data3 = eval(test_data["body"])
                # body_data = dict(data3, **param3)
                body_data = eval(self.data_findall(data_body=data3, fields=param3))
            # 更新url后面的params参数
            elif (test_data["transfer"] != '' or test_data["sql"] != '') and test_data["body"] == '' and \
                    test_data["params"] != '':
                body_data = None
                param1 = eval(test_data["params"])
                if param is not None:
                    params = dict(dict(param2, **param1), **param3)
                else:
                    params = dict(param1, **param3)
            # 不需要更新(params)
            elif test_data["transfer"] == '' and test_data["sql"] == '' and test_data["body"] == '' and \
                    test_data["params"] != '':
                body_data = None
                param1 = eval(test_data["params"])
                if param is not None:
                    params = dict(param2, **param1)
                else:
                    params = param1
            # 不需要更新(body)
            elif test_data["transfer"] == '' and test_data["sql"] == '' and test_data["body"] != '' and \
                    test_data["params"] == '':
                body_data = eval(test_data["body"])
                params = param2
            else:
                body_data = {}
                params = param2
        except Exception as e:
            self.logger.error("读取参数出错！请检查参数格式是否正确！错误信息：{}".format(e))
            raise
        # post请求body类型
        kind = test_data["type"]
        # 判断传data数据还是json
        if kind == "json":
            body = json.dumps(body_data)
        else:
            body = body_data
        self.logger.info("请求body内容为：%s" % body)
        self.logger.info("请求params内容为：%s" % params)
        return body, params

    def send_requests(self, session, test_data, sheet, param=None):
        """
        请求
        :param session: session消息
        :param test_data: 测试数据
        :param sheet: 用例页名称
        :param param:初始化数据
        :return: 测试结果
        """
        self.logger.info("*******正在执行用例：-----  %s  ----**********" % test_data['id'])
        method = test_data["method"]  # 请求方式
        self.logger.info("请求方式：{}".format(method))
        results = {}  # 接受返回数据
        if test_data["url_join"] == "Y":
            url = self.send_url2(sheet, test_data)
            params = param
            body = test_data['body']
        else:
            url = self.send_url(test_data)
            all_data = self.send_body_data(sheet, test_data, param)
            body, params = all_data[0], all_data[1]
        headers = self.send_headers(test_data)
        # 发送请求
        try:
            r = session.request(method=method,
                                url=url,
                                params=params,
                                headers=headers,
                                data=body,
                                verify=False
                                )
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
            self.logger.info("检查点->：%s" % test_data["checkpoint"])
            if test_data["checkpoint"] in results["text"]:
                results["result"], results["msg"] = "pass", ""
                self.logger.info("用例执行成功！页面返回信息：%s" % r.content.decode("utf-8"))
            else:
                results["result"], results["msg"] = "fail", r.content.decode("utf-8")
                self.logger.error("用例执行失败！页面返回信息：%s" % r.content.decode("utf-8"))
            self.logger.info("用例测试结果:   %s---->%s" % (test_data['id'], results["result"]))
            self.logger.info("*******执行用例完成：-----  %s  ----**********\n" % test_data['id'])
            return results
        except Exception as msg:
            self.logger.error("用例执行错误！错误信息：{}".format(msg))
            self.logger.info("*******执行用例完成：-----  %s  ----**********" % test_data['id'])
            results["result"], results["msg"] = "fail", "请求错误！请检查参数设置！"
            results['error'], results['times'] = "", ""
            return results

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
            wt = WriteExcel(filename, sheet)
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


if __name__ == "__main__":
    username = globalparam.username
    password = globalparam.password
    sheet_name = 'Sheet_basic'
    father_path = os.path.abspath(os.path.dirname(os.getcwd()) + os.path.sep + ".")  # 当前文件目录的父级目录
    excelPath = os.path.join(father_path, "Test_File\\测试用例.xlsx")
    data = ExcelUtil(excelPath, sheet_name=sheet_name).dict_data()
    s = requests.session()
    # 用例id
    i = 15
    res = SendRequests().send_requests(s, data[i - 1], sheet_name)
    # field = {'id': 361, "msgTag": "text"}
    # test_data = eval(data[i - 1]["body"])
    # print(SendRequests().data_findall(data_body=test_data, fields=field))
