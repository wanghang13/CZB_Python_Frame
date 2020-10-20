# **************随机字母或数字************
# 支持数字、大小写字母、汉字、邮箱、地址等
# 作者：杭仔
# ****************************************
# -*- coding:UTF-8 -*-
import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import random
from faker import Factory


class Getrand(object):
    def __init__(self):
        self.data_type = 2
        self.head = random.randint(0xb0, 0xf7)
        self.fake = Factory().create('zh_CN')

    def getrand(self, num, data_type=None):  # num 是位数
        """
        获取随机的数字或字母
        :param num: 位数
        :param data_type: 类型，默认数字和字母组合，data_type=2数字组合
        :return:返回随机组合"1231"
        """
        s = ""
        # 随机数字
        if data_type == self.data_type:
            for i in range(num):
                if i == 0:
                    numb = random.randint(1, 9)
                else:
                    numb = random.randint(0, 9)
                s += str(numb)
        # 随机数字、字母组合
        elif data_type is None:
            for i in range(num):
                n = random.randint(1, 2)  # n = 1  生成数字  n=2  生成字母
                if n == 1:
                    numb = random.randint(0, 9)
                    s += str(numb)
                else:
                    nn = random.randint(1, 2)  # n = 1  生成大写  n=2  生成小写
                    cc = random.randint(1, 26)
                    if nn == 1:
                        numb = chr(64 + cc)
                        s += numb
                    else:
                        numb = chr(96 + cc)
                        s += numb
        # 随机字母
        else:
            for i in range(num):
                nn = random.randint(1, 2)
                cc = random.randint(1, 26)
                if nn == 1:
                    numb = chr(64 + cc)
                    s += numb
                else:
                    numb = chr(96 + cc)
                    s += numb
        return s

    # 随机生成汉字
    def get_chinese(self, num):
        """
        获取随机汉字
        :param num: 位数
        :return: 返回随机组合"sdf"
        """
        st = ""
        for i in range(num):
            head = self.head
            body = random.randint(0xa1, 0xf9)  # 在head区号为55的那一块最后5个汉字是乱码,为了方便缩减下范围
            val = f'{head:x}{body:x}'
            st += bytes.fromhex(val).decode('gb2312')
        return st

    def get_chinese1(self, num, num2):
        """
        获取随机汉字
        :param num: 位数
        :param num2: 个数
        :return: "abc,dfd,hgf"
        """
        st = ""
        for j in range(num2):
            st += self.get_chinese(num)
            if j < num2 - 1:
                st += ","
        return st

    def get_chinese_list(self, num, num2):
        """
        获取随机汉字
        :param num: 位数
        :param num2: 个数
        :return: "abc,dfd,hgf"
        """
        list_1 = []
        for j in range(num2):
            list_1.append(self.get_chinese(num))
        return list_1

    # def random_phone_number(self):
    #     """随机手机号"""
    #     return self.fake.phone_number()

    # def random_name(self):
    #     """随机姓名"""
    #     return self.fake.name()

    # def random_address(self):
    #     """随机地址"""
    #     return self.fake.address()

    # def random_email(self):
    #     """随机email"""
    #     return self.fake.email()

    # def random_ipv4(self):
    #     """随机IPV4地址"""
    #     return self.fake.ipv4()

    # def random_str(self, min_chars=0, max_chars=8):
    #     """长度在最大值与最小值之间的随机字符串"""
    #     return self.fake.pystr(min_chars=min_chars, max_chars=max_chars)
