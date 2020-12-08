# ****************读取用例*****************
# 读取所有的测试用例
# 保存在list里
# 作者：杭仔
# *****************************************
# -*- coding:UTF-8 -*-
import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import openpyxl
import xlrd
import os
import requests
import json
from Common import Log
from Common import globalparam



class ExcelUtil(object):
    def __init__(self, path, sheet_name="Sheet3"):
        """
        :param path: excel地址
        :param sheet_name: sheet名称，默认为Sheet1
        """
        self.keys = []
        self.logger = Log.TestLog()
        # self.data = openpyxl.load_workbook(path)
        self.data = xlrd.open_workbook(path)
        self.table = self.data.sheet_by_name(sheet_name)

        # 获取第一行作为key值
        self.keys = self.table.row_values(2)
        # 获取总行数
        self.rowNum = self.table.nrows
        # 获取总列数
        self.colNum = self.table.ncols
        # print(self.data,self.table,self.keys,self.rowNum,self.colNum)

    def GetRowsListData(self,line):
        keys = []
        for value in list(self.table.rows)[line-1]:
            keys.append(value.value)
        return keys
    # 读取excel数据
    def dict_data(self):
        """"
        读取excel表结果为dict
        第一行为字典的key，下面的为值
        return [{'title':'1','user':'root'},{'title':'2','user':'xiaoshitou'}]
        """
        try:
            if self.rowNum <= 1:
                self.logger.error("总行数小于1,请检查用例文件是否正确！")
            else:
                # url = self.table.cell_value(2,1)
                result = []  # 结果
                for line in list(range(2,self.rowNum - 1)):
                    value = {}
                    # 从第二行取对应values值
                    # value['url'] = url
                    value['rowNum'] = line
                    values = self.table.row_values(line + 1)
                    for x in list(range(0, self.colNum)):
                        value[self.keys[x]] = values[x]
                    result.append(value)
                if len(result) == 0:
                    self.logger.error("未读取到测试用例！")
                return result
        except Exception as e:
            self.logger.error("错误信息:{}".format(e))

    def get_xls_to_dict(self):
        """
        读取excel表结果为dict
        第一行为字典的key，下面的为值
        return [{'title':'1','user':'root'},{'title':'2','user':'xiaoshitou'}]
        """
        dataresult = [self.table.row_values(j) for j in range(2, self.table.nrows)]
        result = [dict(zip(dataresult[0], dataresult[f])) for f in range(1, len(dataresult))]
        return result

if __name__ == "__main__":
    # print(globalparam.data_path)
    path = globalparam.data_path+'/日常冒烟测试点.xlsx'
    s = ExcelUtil(path).get_xls_to_dict()
    e = ExcelUtil(path).dict_data()
    print(e)
    # s = requests.session()
    # print(s)
    # for d in e:
    #     r = s.request(method=d['method'],url = d['url'],headers=eval(d['headers']),data=json.dumps(eval(d['data'])),verify=False)
    #     print(d['url'])
    #     print(json.dumps(eval(d['data'])))
    #     print(r.json()['status'],r.json()['info'])

    # s.request()