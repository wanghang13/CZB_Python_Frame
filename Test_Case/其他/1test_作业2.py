import sys,os
import pytest
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from  Common.Write_Config_Info import Write_Config
from Common import globalparam

# class 
def test_Run_Unittest_Main(excel_name,sheet_name):
# def test_Run_Unittest_Main():
    # write_excel_info(excel_name,sheet_name)
    Write_Config().write_excel_info(excel_name,sheet_name)
    # Write_Config().write_excel_info('Test_Case.xlsx','Sheet4')
    os.system(f'pytest -v {globalparam.pytest_main}')

if __name__ == "__main__":
    test_Run_Unittest_Main('Test_Case.xlsx','Sheet4')
# Write_Config().write_excel_info('Test_Case.xlsx','Sheet4')