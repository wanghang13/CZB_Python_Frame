

# 1、Common         文件夹  放入框架的所有基础的方法。如：requests库 方法，读取excel、写入excel、log日志写入的方法等。
# 2、Test_Case      文件夹  放入Excel测试用例。
# 3、Test_Config    文件夹  存放相应配置文件。
# 4、Test_File      文件夹  存放执行用例py文件
# 5、Test_Report    文件夹  存放导出报告和日志文件
# 6、run_all.py        文件  主程序文件执行相应case 内容。


from Common import globalparam
from Common import Log

logger = Log.TestLog()

logger.info('测试log 方法写入。')


# print(globalparam.prj_path)