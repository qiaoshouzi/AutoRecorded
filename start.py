#import
import os
import sys
import time
import json
import requests
import random
import logging
import logging.handlers

#变量
universalCounter=0 #通用计数器

live_cid="" #直播间房间号
live_platform="web" #直播流格式
live_quality="4" #画质 2：流畅 3：高墙 4：原画
live_qn="10000" #画质 80：流畅 150：高墙 400：蓝光 10000：原画
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

recordingFolder="" #录播文件存储目录

ffmpeg_location="ffmpeg.exe" #ffmpeg.exe 文件位置
ffmpeg_UA="User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36" #headers UA 保证不会403

#初始化
 #日志初始化
  #初始化
logging.basicConfig(level = logging.INFO,format = '%(lineno)d | %(asctime)s - %(name)s - %(levelname)s - %(message)s') #设置控制台显示log的样式
  #创建
logger = logging.getLogger("AutoRecorded")
  #创建handler
handler1 = logging.FileHandler("log\\log-"+str(int(time.time()))+".log") #设置log文件名格式
handler1.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s|%(name)-12s+ %(levelname)-8s++%(message)s') #设置 log文件 显示log的样式
handler1.setFormatter(formatter)
handler2 = logging.StreamHandler()
handler2.setLevel(logging.ERROR)
logger.addHandler(handler1)
logger.addHandler(handler2)


#主代码
universalCounter = 0 #计数器归0
logger.info("开始运行")
while 1 == 1:
    #如果计数器 == 1，代表ffmpeg已关闭，输出log并等待30s的冷却期
    if universalCounter == 1:
        logger.info("检测到ffmpeg意外关闭/已下播，循环重新开始")
        universalCounter = 0
        time.sleep(30)
    #检测是否开播，如果开播抓取直播源并使用ffmpeg进行录播
    while 1 == 1:
        live_state=requests.post(api_post_live_inf, api_post_live_inf_json).json() #获取直播详细 json
        i=live_state['code']
        if i == -412: #检测是否被IP临时BAN，冷却5min
            logger.error("IP被拦截，已自动等待5min")
            time.sleep(300)
        live_state=live_state["data"]["live_status"] #获取直播间状态码 0 未开播 1 开播
        if live_state == 1:
            logger.info("检测到开播")
            live_url = requests.get(api_get_live_feeds, api_get_live_feeds_json).json() #获取直播源URL json
            live_url = live_url["data"]["durl"][0]["url"] #获取直播源URL
            logger.info("获取到直播源: "+live_url)
            logger.info("ffmpeg已打开，录播开始")
            file_name = str(int(time.time())) #将当前时间戳设置为录播文件名
            recordingFolder = recordingFolder+file_name+".flv"
            os.system(ffmpeg_location+' -headers "'+ffmpeg_UA+'" -i "'+live_url+'" -c copy '+recordingFolder)
            universalCounter = 1 #将计数器设置为1确保能识别
            break
        time.sleep(30)