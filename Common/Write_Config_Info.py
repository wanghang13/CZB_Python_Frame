

import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# print(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from configobj import ConfigObj
from Common import globalparam

class Write_Config():

    def __init__(self):
        self.config = ConfigObj(globalparam.config_path,encoding='UTF8')

    def write_excel_info(self,excel_name,sheet_name):
        self.config['EXCEL_INFO']['excel_name'] = excel_name
        self.config['EXCEL_INFO']['sheet_name'] = sheet_name
        self.config.write()

    def Switch_Host(self,host = '正式'):
        if host == "Release" or host == '0' or host == '正式':
            self.config['RUN_API']['MP_NLSAAS'] = self.config['MP_NLSAAS']['url_Release'] 
            self.config['RUN_API']['POS_API'] = self.config['POS_API']['url_Release']
            self.config['RUN_API']['POS_OS_API'] = self.config['POS_OS_API']['url_Release']
            self.config['RUN_API']['POS_SELF_API'] = self.config['POS_SELF_API']['url_Release']
        elif host == "test" or host == '1' or host == '测试':
            self.config['RUN_API']['MP_NLSAAS'] = self.config['MP_NLSAAS']['url_Test'] 
            self.config['RUN_API']['POS_API'] = self.config['POS_API']['url_Test']
            self.config['RUN_API']['POS_OS_API'] = self.config['POS_OS_API']['url_Test']
            self.config['RUN_API']['POS_SELF_API'] = self.config['POS_SELF_API']['url_Test']
        elif host == "Pre-release" or host == '2' or host == '预发布':
            self.config['RUN_API']['MP_NLSAAS'] = self.config['MP_NLSAAS']['url_Pre-release'] 
            self.config['RUN_API']['POS_API'] = self.config['POS_API']['url_Pre-release']
            self.config['RUN_API']['POS_OS_API'] = self.config['POS_OS_API']['url_Pre-release']
            self.config['RUN_API']['POS_SELF_API'] = self.config['POS_SELF_API']['url_Pre-release']
        elif host == "Green-Release" or host == '3' or host == '绿色':
            self.config['RUN_API']['MP_NLSAAS'] = self.config['MP_NLSAAS']['url_Green-release'] 
            self.config['RUN_API']['POS_API'] = self.config['POS_API']['url_Green-release']
            self.config['RUN_API']['POS_OS_API'] = self.config['POS_OS_API']['url_Green-release']
            self.config['RUN_API']['POS_SELF_API'] = self.config['POS_SELF_API']['url_Green-release']
        elif host == "Blue-Release" or host == '4' or host == '蓝色':
            self.config['RUN_API']['MP_NLSAAS'] = self.config['MP_NLSAAS']['url_Blue-release'] 
            self.config['RUN_API']['POS_API'] = self.config['POS_API']['url_Blue-release']
            self.config['RUN_API']['POS_OS_API'] = self.config['POS_OS_API']['url_Blue-release']
            self.config['RUN_API']['POS_SELF_API'] = self.config['POS_SELF_API']['url_Blue-release']
        self.config.write()

# Write_Config().Switch_Host('1')
# config = ConfigObj(globalparam.config_path,encoding='UTF8')
# print(config['RUN_API']['MP_NLSAAS'] )
# print(config['RUN_API']['POS_API'] )
# print(config['RUN_API']['POS_OS_API'] )
# print(config['RUN_API']['POS_SELF_API'])