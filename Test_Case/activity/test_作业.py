# *****************测试用例***************
# 利用ddt数据驱动
# 作者：杭仔
# ***************************************
# -*- coding:UTF-8 -*-
import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import requests
import unittest
import warnings
from Common import ddt_new
from Common.Read_File import ExcelUtil
from Common.RequestsSend import SendRequests
from Common.Log import TestLog
from Common.Initial import Initials
from Common import globalparam

reportPath = globalparam.report_path 
# 读取和写入的表格名称
# sheet_name = globalparam.sheet_basic
excel_name = 'Test_Case.xlsx'
sheet_name = "Sheet3"
excelPath = os.path.join(globalparam.prj_path, 'Test_File', excel_name)

# print(excelPath,reportPath,sheet_name)
# 读取测试用例
# test_data = ExcelUtil(excelPath, sheet_name=sheet_name).dict_data()[38:39:1]
test_data = ExcelUtil(excelPath, sheet_name=sheet_name).dict_data()
logger = TestLog()


@ddt_new.ddt
class TestApi(unittest.TestCase):
    """基础接口"""

    @classmethod
    def setUpClass(cls):
        cls.session = requests.session()
        warnings.simplefilter('ignore',ResourceWarning)
        # 先复制excel数据到report
        # Write_Excel.copy_excel(excelPath, reportPath)  # 复制xlsx
        # Write_Excel.copy_file(excelPath, reportPath)    # 复制xlsx

    @ddt_new.data(*test_data)
    def test_member(self, data):
        """
        执行测试
        :param data:excel数据
        :return:
        """        
        logger.info("********************************************************************************")
        # 请求        
        results = SendRequests().send_requests(self.session, data ,test_data)
        # 写入测试数据
        # SendRequests().wirte_result(results, filename=reportPath, sheet=sheet_name)
        # 检查点 checkpoint
        check = data["checkstatus"]
        # print(type(check))
        # 返回结果
        res_status = str(results['json']['status'])
        # print(type(res_status))
        # 断言
        self.assertEqual(check, res_status)
        # self.assertTrue(check in res_status)
        # self.assertIn(check, res_text)
        logger.info("********************************************************************************")

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == "__main__":
    unittest.main()
