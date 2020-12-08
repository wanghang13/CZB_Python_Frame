# *****************测试用例***************
# 利用ddt数据驱动
# 作者：杭仔
# ***************************************
# -*- coding:UTF-8 -*-

import requests
import unittest
import warnings
import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from Common import ddt_new
from Common.Read_File import ExcelUtil
from Common.RequestsSend import SendRequests
from Common.Log import TestLog
from Common.Initial import Initials
from Common import globalparam
from Common import Write_Excel
from configobj import ConfigObj
from Common import Log

reportPath = globalparam.report_path 

# 读取和写入的表格名称
excel_name = '日常冒烟测试点.xlsx'
sheet_name = "商户后台接口冒烟" 
excelPath = os.path.join(globalparam.prj_path, 'Test_File', excel_name)
report_path = os.path.join(globalparam.prj_path, 'Test_Report','excel_report',excel_name)
init_report_path = os.path.join(globalparam.prj_path, 'Test_Report','excel_report',"init_" + excel_name)
 
# 读取测试用例
test_data = ExcelUtil(excelPath, sheet_name=sheet_name).dict_data()
logger = TestLog()


@ddt_new.ddt
class TestApi(unittest.TestCase):
    """基础接口"""

    @classmethod
    def setUpClass(self):
        self.logger = Log.TestLog()
        self.session = requests.session()
        warnings.simplefilter('ignore',ResourceWarning)
        Write_Excel.copy_excel(excelPath,init_report_path)
        

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
        SendRequests().wirte_result(results, filename=excelPath, sheet=sheet_name)
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
    def tearDownClass(self):
        pass
        self.config = ConfigObj(globalparam.config_path,encoding='UTF8')
        if self.config['EXCEL_INFO']['Excel_Save'] == '1':
            # 先复制excel数据到report
            Write_Excel.copy_excel(excelPath,report_path)  # 复制xlsx
        # Write_Excel.copy_file(excelPath, reportPath)    # 复制xlsx

if __name__ == "__main__":
    unittest.main()
