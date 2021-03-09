#import
import logging
import logging.handlers
import requests
import time

#初始化
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

class serverChan:
  def push(serverChan_SendKey, serverChan_title):
    serverChan_returnValue=requests.post("https://sctapi.ftqq.com/"+serverChan_SendKey+".send?title="+serverChan_title).json()
    serverChan_code=serverChan_returnValue["code"]
    serverChan_pushid=serverChan_returnValue["data"]["pushid"]
    serverChan_readkey=serverChan_returnValue["data"]["readkey"]
    if serverChan_code == 0:
      logger.info(" [方糖推送] 推送成功")
      logger.info("pushid="+serverChan_pushid+"  readkey="+serverChan_readkey)
    # <TODO> 复查系统
    if serverChan_code == 40001:
        serverChan_info=serverChan_returnValue["info"]
        logger.error(serverChan_info)
    if serverChan_code == 20001:
        serverChan_info=serverChan_returnValue["info"]
        logger.error(serverChan_info)