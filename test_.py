

# 前置操作：拷贝框架内的Read_File.py 、Log.py 和 日常冒烟测试点.xlsx 三个文件 到  上节课作业 的 目录中。

# 1、调用 Read_File.py 文件 来读取 日常冒烟测试点.xlsx 的任意的 case。

# 2、将读取的case 进行 requests 接口 测试。

# 3、将接口 返回做校验 并调用log.py 文件 写入相应的日志信息。
import os,sys
from Common.Read_File import ExcelUtil
from Common import globalparam

excel_path = os.path.join(globalparam.data_path,'日常冒烟测试点.xlsx')
print(excel_path)

data = ExcelUtil(excel_path,'Test').dict_data()
print(len(data))