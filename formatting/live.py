#import
from requests.api import request
from .plugins.qqAPI import qqGroup
from .plugins.serverChan import serverChan
import logging
import logging.handlers
import time
import requests
import os
import sys

#公共变量
serverChan_SendKey = '' #server酱 key #必填
live_cid = '' #直播间房间号 #必填
api_get_live_url='http://api.live.bilibili.com/room/v1/Room/playUrl' #获取 直播源URL 的API
api_get_live_url_json={
    'cid': live_cid,
    'qn': '4',
    #'quality': '10000',
    'platform': 'web'
}
api_post_live_inf='https://api.live.bilibili.com/room/v1/Room/room_init' #获取 直播间信息 的API
api_post_live_inf_json={
    'id': live_cid
}

live_storageLocation=r'' #录播文件存储目录 #必填

live_ffmpegLocation=r'' #启动ffmpeg的参数 win为文件的绝对路径(ffmpeg.exe) linux为启动指令(ffmpeg)  #必填
live_ffmpegUA="User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36" #headers UA 保证不会403 #选填

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

def log_And_ft(log_type, inf_content):
    if log_type == 'info':
        logger.info(inf_content)
    if log_type == "error":
        logger.error(inf_content)
    serverChan.push(serverChan_SendKey, inf_content)

def Auto_REC_Live():
    live_ffmpegState = False #ffmpeg状态初始化
    logger.info('[Auto_Live] 开始运行')
    while True:
        if live_ffmpegState == True:
            log_And_ft('info', '[Auto_Live][警告] 检测到ffmpeg意外关闭/已下播，循环重新开始')
            live_ffmpegState = False
            time.sleep(30)
        while True:
            live_state=requests.post(api_post_live_inf, api_post_live_inf_json).json()
            i=live_state['code']
            if i == -412: #检测是否被IP临时BAN，冷却5min
                log_And_ft('error', '[Auto_Live][错误] IP被拦截，已自动等待5min')
                time.sleep(300)
            live_state=live_state['data']['live_status'] #获取直播间状态码 0 未开播 1 开播
            if live_state == 1:
                log_And_ft('info', '[Auto_Live] 检测到开播')
                live_url = requests.post(api_get_live_url, api_get_live_url_json).json()
                live_url = live_url['data']['durl'][0]['url']
                logger.info("[Auto_Live] 获取到直播源: "+live_url)
                logger.info("[Auto_Live] ffmpeg已打开，录播开始")
                live_storageName = str(int(time.time()))+'.flv' #将当前时间戳设置为录播文件名
                time.sleep(60)
                os.system(live_ffmpegLocation+' -headers "'+live_ffmpegUA+'" -i "'+live_url+'" -c copy '+live_storageLocation+live_storageName)
                live_ffmpegState = True
                break
            time.sleep(30)