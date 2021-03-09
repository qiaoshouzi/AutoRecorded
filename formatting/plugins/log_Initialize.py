#import
import logging
import logging.handlers
import time

def Initialize():
     #初始化
    logging.basicConfig(level = logging.INFO,format = '%(lineno)d | %(asctime)s - %(name)s - %(levelname)s - %(message)s') #设置控制台显示log的样式
     #创建
    logger = logging.getLogger("AutoRecorded")
     #创建handler
    handler1 = logging.FileHandler("logs\\log-"+str(int(time.time()))+".log") #设置log文件名格式
    handler1.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s|%(name)-12s+ %(levelname)-8s++%(message)s') #设置 log文件 显示log的样式
    handler1.setFormatter(formatter)
    handler2 = logging.StreamHandler()
    handler2.setLevel(logging.ERROR)
    logger.addHandler(handler1)
    logger.addHandler(handler2)