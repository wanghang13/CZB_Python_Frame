import pytest
import os
import time
from Common.globalparam import allure_dir,allure_plus_dir
if __name__ == "__main__":
    pass
    # case_name = ['test_run.py']
    # for case in case_name:
    #     os.system('pytest Test_Case/'+case)

    # os.system('pytest  -v Test_Case/test_run.py')
    report_file = time.strftime("%Y-%m-%d")
    # os.system(f'python3 -m pytest  -v  Test_Case/其他 --html=Test_Report/{report_file}-report.html')
    # os.system("pytest -v --alluredir ./Test_Report/alluredir")
    # os.system("pytest -v -k test_作业.py --alluredir ./Test_Report/allureTest_Report")
    # os.system("python3 -m pytest  -v -k test_作业.py")

    # os.system('allure generate Test_Report/alluredir --clean')
    # # pytest.main()
    # allure测试报告存放路径
    allure_path = os.path.join(allure_dir, report_file)
    # allure-plus测试报告存放路径
    allure_plus_path = os.path.join(allure_plus_dir, report_file)
    

    pytest.main(["-v", f"--alluredir={allure_path}"])
    os.system(f"allure generate {allure_path} -o {allure_plus_path} --clean")
    os.system(f'allure serve {allure_path}')
    # print()

    