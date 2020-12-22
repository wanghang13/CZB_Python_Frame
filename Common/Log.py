# ****************LOG配置*****************
# 作者：杭仔
# *****************************************
# -*- coding:UTF-8 -*-

import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Common import globalparam
import time
import logging
log_path = globalparam.log_path


# ch = logging.StreamHandler()



class TestLog(object):
    def __init__(self):
        # 日志文件的存放路径，根据自己的需要去修改
        self.test_report = globalparam.log_path
        self.now = time.strftime("%Y-%m-%d-")
        self.log_file_path = self.test_report + "/" + self.now + '-log_result.log'
        
    def __printconsole(self, level, message):
        # 创建一个logger
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        # 创建一个handler，用于写入日志文件
        fh = logging.FileHandler(self.log_file_path, 'a+', encoding='utf-8')
        fh.setLevel(logging.INFO)
        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        # 定义handler的输出格式
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        # 给logger添加handler
        if not logger.handlers:
            logger.addHandler(fh)
            logger.addHandler(ch)
        # 记录一条日志
        if level == 'info':
            logger.info(message)
        elif level == 'debug':
            logger.debug(message)
        elif level == 'warning':
            logger.warning(message)
        elif level == 'error':
            logger.error(message)
        logger.handlers.clear()
        # # 关闭打开的文件
        fh.close()

    def debug(self, message):
        self.__printconsole('debug', message)

    def info(self, message):
        self.__printconsole('info', message)

    def warning(self, message):
        self.__printconsole('warning', message)

    def error(self, message):
        self.__printconsole('error', message)
