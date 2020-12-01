# ****************配置路径*****************
# 配置基础路径信息
# 作者：杭仔
# *****************************************
# -*- coding:UTF-8 -*-
import os

# 项目参数设置
prj_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 日志路径
log_path = os.path.join(prj_path, 'Test_Report','log')
# 测试报告存放路径
report_dir = os.path.join(prj_path, "Test_Report")

# Unittest主程序文件路径
unittest_main = os.path.join(prj_path, "Common",'Unittest_Main.py')

# Pytest主程序文件路径
pytest_main = os.path.join(prj_path, "Common",'Pytest_Main.py')

# Allure测试报告存放路径
allure_dir = os.path.join(report_dir, "allure")

# Allure_Plus测试报告存放路径
allure_plus_dir = os.path.join(report_dir, "allure_plus")

# 测试报告路径
report_path = os.path.join(prj_path, 'Test_Report', '测试用例执行结果.xlsx')
# 测试数据路径
data_path = os.path.join(prj_path, 'Test_File')
data_path_file = os.path.join(prj_path, 'Test_File', 'Test_Case.xlsx')
# 配置文件路径
config_path = os.path.join(prj_path, "Test_Config", "config.ini")
# 存放用例文件名称的文件路径
caseListFile = os.path.join(prj_path, 'Test_Config', 'caseListFile.txt')

# 要执行的测试用例目录
test_dir = os.path.join(prj_path, 'Test_Case')
# 存放用例文件名称的文件路径
caseListFile = os.path.join(prj_path, 'Test_File', 'caseListFile.txt')

# 商户后台账号
username = 'hang0813'
password = 'wh0813'
