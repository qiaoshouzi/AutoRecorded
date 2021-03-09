#import
from . import plugins
import os
import sys
import time
import json
import requests
import random
import logging
import logging.handlers

#插件开关
plug_serverChan=False #是否开启 Server酱 推送 如果开启了一定要填写 否则可能会报错
plug_qqAPI=False #是否开启 qqAPI 推送 如果开启了一定要填写 否则可能会报错

#变量

#日志初始化
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

#def
 #方糖
def ftqq(ftqq_SendKey, ftqq_title):
    if plug_serverChan == True:
        plugins.plug_serverChan_push(ftqq_SendKey, ftqq_title)
    else:
        logger.info("[方糖推送] 未开启，推送失败")
 #QQ推送
def qqAPI(ftqq_SendKey):
    if plug_qqAPI == True:
        plugins.plug_qqAPI_groupPush(ftqq_SendKey)
    else:
        logger.info("[qqAPI推送] 未开启，推送失败")

#主代码
logger.info("[BOT] 开始运行")
