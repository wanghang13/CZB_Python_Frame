# ****************读取配置文件*****************
# 作者：杭仔
# *****************************************
# -*- coding:UTF-8 -*-
import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import configparser
from Common import globalparam


class ReadConfig(object):
    def __init__(self):
        # self.father_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # self.config_path = os.path.join(self.father_path, "Test_File", "config.ini")
        self.config_path = globalparam.config_path
        self.cp = configparser.ConfigParser()
        self.cp.read(self.config_path, encoding="utf-8-sig")

    def read_mysql(self, name):
        """
        读取数据库配置
        :param name: 配置文件标签名称
        :return: 数据库配置
        """
        db = {}
        key = ['localhost', 'username', 'password', 'database']
        for i in key:
            value = self.cp.get(name, i)
            db[i] = value
        return db

    def read_ip(self):
        """读取服务地址"""
        ip_address = self.cp.get("HTTP", "url")
        return ip_address

    def read_email(self, name):
        """
        读取邮件配置
        :param name: 配置文件标签名称
        :return: 邮件配置
        """
        read_email = {}
        key = ['msg_from', 'pass_wd', 'msg_to', 'server']
        for i in key:
            value = self.cp.get(name, i)
            read_email[i] = value
        return read_email

    def read_log(self):
        """读取日志配置"""
        read_log = self.cp.get("LOG", "level")
        return read_log

    def get_value(self, env, name):
        """
        [projectConfig]
        :param env:[projectConfig]
        :param name:project_path
        """
        return self.cp.get(env, name)

if __name__ == "__main__":
    s = ReadConfig().read_email('EMAIL')
    print(s)