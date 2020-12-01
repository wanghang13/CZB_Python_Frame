# *****************测试用例***************
# 利用ddt数据驱动
# 作者：杭仔
# ***************************************
# -*- coding:UTF-8 -*-
import sys,os
import pytest
# sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# print(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# quit()
import requests
import unittest
import warnings
from configobj import ConfigObj
from Common import ddt_new
from Common.Read_File import ExcelUtil
from Common.RequestsSend import SendRequests
from Common.Log import TestLog
from Common.Initial import Initials
from Common import globalparam
from Common import Write_Excel
from configobj import ConfigObj
import pytest

config = ConfigObj(globalparam.config_path,encoding='UTF8')
# reportPath = globalparam.report_path 
# 读取和写入的表格名称
excel_name = config['EXCEL_INFO']['excel_name']
sheet_name = config['EXCEL_INFO']['sheet_name']
excelPath = os.path.join(globalparam.prj_path, 'Test_File', excel_name)
report_path = os.path.join(globalparam.prj_path, 'Test_Report','excel_report',excel_name)
# 读取测试用例
test_data = ExcelUtil(excelPath, sheet_name=sheet_name).dict_data()
# print(test_data)
# print(len(test_data))
# quit()
logger = TestLog()

# @ddt_new.ddt
class TestApi():
    """基础接口"""

    def setup(self):
        self.session = requests.session()
        self.config = ConfigObj(globalparam.config_path,encoding='UTF8')
        warnings.simplefilter('ignore',ResourceWarning)


    @pytest.mark.parametrize('data' , test_data) 
    def test_member(self, data):
        """
        执行测试
        :param data:excel数据
        :return:
        """        
        test_data = data
        logger.info("********************************************************************************")
        # 请求        
        results = SendRequests().send_requests(self.session, data ,test_data)
        # 写入测试数据
        SendRequests().wirte_result(results, filename=excelPath, sheet=sheet_name)
        # 检查点 checkstatus
        check = data["checkstatus"]
        # 返回结果
        res_status = str(results['json']['status'])
        # print(type(res_status))
        # 断言
        assert check == res_status
        # self.assertEqual(check, res_status)
        # self.assertTrue(check in res_status)
        # self.assertIn(check, res_text)
        logger.info("********************************************************************************")

    def teardown(self):
        pass
        if self.config['EXCEL_INFO']['Excel_Save'] == '1':
            # 先复制excel数据到report
            Write_Excel.copy_excel(excelPath,report_path)  # 复制xlsx
        # Write_Excel.copy_file(excelPath, reportPath)    # 复制xlsx

# if __name__ == "__main__":
#     TestApi().test_member(test_data)
