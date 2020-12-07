# import pytest
import os
import time
from Common.globalparam import allure_dir,allure_plus_dir
from  Common.Write_Config_Info import Write_Config

if __name__ == "__main__":
    # os.system('pytest  -v Test_Case/test_run.py')
    report_file = time.strftime("%Y-%m-%d")
    # os.system(f'pytest  -v  Test_Case/其他 --html=Test_Report/report/{report_file}-report.html')
    # os.system("pytest -v --alluredir ./Test_Report/alluredir")
    # os.system("python3 -m pytest  -v -k test_作业.py")

    # os.system('allure generate Test_Report/alluredir --clean')
    # pytest.main() 


    # allure测试报告存放路径
    allure_path = os.path.join(allure_dir, report_file)
    # allure-plus测试报告存放路径
    allure_plus_path = os.path.join(allure_plus_dir, report_file)

    '''
    切换测试环境地址调用：Write_Config().Switch_Host() 方法。
    默认不传参 为正式环境。
    测试环境传递： 1 OR 测试 OR test 
    预发布环境传递： 2 OR 预发布 OR Pre-release 
    绿色域名环境传递：3 OR 绿色 OR Green-Release
    绿色域名环境传递：4 OR 蓝色 OR Blue-Release
    正式环境传递： 0 OR 不传递
    '''
    
    Write_Config().Switch_Host('1')
# 
    # os.system(f'pytest  -v Test_Case/test_return_point --html=Test_Report/report/{report_file}-report.html')
    os.system(f'pytest  -v  -k test_双屏机常用接口冒烟.py --html=Test_Report/report/{report_file}-report.html')
    # os.system(f'pytest  -v  -k test_商户后台常用接口冒烟.py --html=Test_Report/report/{report_file}-report.html')
    # os.system(f'pytest  -v  -k test_POS机常用接口冒烟.py --html=Test_Report/report/{report_file}-report.html')
    # os.system(f"pytest -v -k test_双屏机常用接口冒烟.py  --alluredir={allure_path}")
    # os.system(f"pytest -v -k test_POS机常用接口冒烟.py  --alluredir={allure_path}")

    # os.system(f"pytest -v  Test_Case/test_return_point  --alluredir={allure_path}")


    # os.system(f"pytest -v -k test_双屏机常用接口冒烟.py --alluredir={allure_path}")
    # # pytest.main(["-v","-k","test_双屏机常用接口冒烟.py","--workers=2", "--tests-per-worker=2" f"--alluredir={allure_path}"])
    # os.system(f"allure generate {allure_path} -o {allure_plus_path} --clean")
    # os.system(f'allure serve {allure_path}')
    # # # # # # # print()

    
