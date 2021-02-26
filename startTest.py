#import
import os
import sys
import time
import json
import requests
import random
import logging
import logging.handlers

#功能开关
switch_ftqq=False #是否开启方糖推送 如果开启了一定要填写 ftqq_SendKey 否则可能会报错

#变量
universalCounter=0 #通用计数器

live_cid="" #直播间房间号 #必填
live_platform="web" #直播流格式 #选填
live_quality="4" #画质 2：流畅 3：高墙 4：原画 #选填
live_qn="10000" #画质 80：流畅 150：高墙 400：蓝光 10000：原画 #选填
live_url="" #直播源url
live_state="" #直播间状态码 0 1

api_get_live_feeds="http://api.live.bilibili.com/room/v1/Room/playUrl" #获取 直播源URL 的API
api_get_live_feeds_json={
    'cid': live_cid,
    'qn': live_qn,
    #'quality': live_quality,
    'platform': live_platform
}
api_post_live_inf="https://api.live.bilibili.com/room/v1/Room/room_init" #获取 直播间信息 的API
api_post_live_inf_json={
    'id': live_cid
}

recordingFolder="" #录播文件存储目录 #必填

ffmpeg_location="" #ffmpeg.exe 文件位置  #必填
ffmpeg_UA="User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36" #headers UA 保证不会403 #选填

ftqq_SendKey="" #方糖的SendKey #必填
ftqq_returnValue="" #返回值
ftqq_code="" #状态信息
ftqq_info="" #错误信息
ftqq_title="" #发送信息的title
ftqq_pushid="" #用来检查
ftqq_readkey="" #用来检查
ftqq_check_returnValue="" #检查_返回值
ftqq_check_code="" #检查_code
ftqq_check_data="" #检查_data信息
ftqq_check_message="" #检查_错误信息

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

#def
 #方糖推送
def ftqqTurbo(ftqq_SendKey, ftqq_title):
    if switch_ftqq==True:
        ftqq_returnValue=requests.post("https://sctapi.ftqq.com/"+ftqq_SendKey+".send?title="+ftqq_title).json()
        ftqq_code=ftqq_returnValue["code"]
        ftqq_pushid=ftqq_returnValue["data"]["pushid"]
        ftqq_readkey=ftqq_returnValue["data"]["readkey"]
        if ftqq_code == 0:
            logger.info(" [方糖推送] 推送成功")
            logger.info("pushid="+ftqq_pushid+"  readkey="+ftqq_readkey)
            while 1==1:
                ftqq_check_returnValue=requests.post("https://sctapi.ftqq.com/push?id="+ftqq_pushid+"&readkey="+ftqq_readkey).json()
                ftqq_check_code=ftqq_check_returnValue["code"]
                ftqq_check_message=ftqq_check_returnValue["message"]
                ftqq_check_data=ftqq_check_returnValue["data"]
                if ftqq_check_code == 10001:
                    logger.error(" [方糖推送复查] 报错10001 错误信息: "+ftqq_check_message)
                    break
                else:
                    if ftqq_check_data == None:
                        logger.error(" [方糖推送复查] data空白，可能pushid/readkey出现问题")
                        break
                    else:
                        if ftqq_check_code["id"] == ftqq_pushid:
                            logger.info(" [方糖推送复查] 推送成功")
                            break
                        else:
                            logger.error(" [方糖推送复查] 未知错误，返回值: "+ftqq_check_returnValue)
                            break
        if ftqq_code == 40001:
            ftqq_info=ftqq_returnValue["info"]
            logger.error(ftqq_info)
        if ftqq_code == 20001:
            ftqq_info=ftqq_returnValue["info"]
            logger.error(ftqq_info)
    else:
        logger.info(" [方糖推送] 未开启方糖推送功能，推送失败")

#主代码
universalCounter = 0 #计数器归0
logger.info(" [BOT] 开始运行")
while 1 == 1:
    #如果计数器 == 1，代表ffmpeg已关闭，输出log并等待30s的冷却期
    if universalCounter == 1:
        logger.info(" [警告] 检测到ffmpeg意外关闭/已下播，循环重新开始")
        ftqqTurbo(ftqq_SendKey, "[警告] 检测到ffmpeg意外关闭/已下播，循环重新开始")
        universalCounter = 0
        time.sleep(30)
    #检测是否开播，如果开播抓取直播源并使用ffmpeg进行录播
    while 1 == 1:
        live_state=requests.post(api_post_live_inf, api_post_live_inf_json).json() #获取直播详细 json
        i=live_state['code']
        if i == -412: #检测是否被IP临时BAN，冷却5min
            logger.error(" [错误] IP被拦截，已自动等待5min")
            ftqqTurbo(ftqq_SendKey, "[错误] IP被拦截，已自动等待5min")
            time.sleep(300)
        live_state=live_state["data"]["live_status"] #获取直播间状态码 0 未开播 1 开播
        if live_state == 1:
            logger.info(" [BOT] 检测到开播")
            ftqqTurbo(ftqq_SendKey, "[BOT] 检测到开播")
            live_url = requests.get(api_get_live_feeds, api_get_live_feeds_json).json() #获取直播源URL json
            live_url = live_url["data"]["durl"][0]["url"] #获取直播源URL
            logger.info(" [BOT] 获取到直播源: "+live_url)
            logger.info(" [BOT] ffmpeg已打开，录播开始")
            file_name = str(int(time.time())) #将当前时间戳设置为录播文件名
            recordingFolder = recordingFolder+file_name+".flv"
            os.system(ffmpeg_location+' -headers "'+ffmpeg_UA+'" -i "'+live_url+'" -c copy '+recordingFolder)
            universalCounter = 1 #将计数器设置为1确保能识别
            break
        time.sleep(30)