#import
import os
import sys
import time
import json
import requests
import random
'''
import psutil
def proc_exist(process_name):
    pl = psutil.pids()
    for pid in pl:
        if psutil.Process(pid).name() == process_name:
            return pid
'''

#变量
universalCounter=0 #通用计数器
 #<相关信息>#
live_cid="1221274" #直播间房间号
live_platform="web" #直播流格式
live_quality="4" #画质 2：流畅 3：高墙 4：原画
live_qn="10000" #画质 80：流畅 150：高墙 400：蓝光 10000：原画
live_url="" #直播源url
  #测试源 https://www.natfrp.com/admin/flower.mp4
live_state=""
#</相关信息>#
 #<API>#
get_live_feeds="http://api.live.bilibili.com/room/v1/Room/playUrl" #直播源
get_live_feeds_json={
    'cid': live_cid,
    'qn': live_qn,
    #'quality': live_quality,
    'platform': live_platform
}
get_live_inf="https://api.live.bilibili.com/room/v1/Room/room_init" #直播信息
get_live_inf_json={
    'id': live_cid
}
#</API>#
 #<相关位置>#
recorded_file_storage="D:\\OBS录像\\ffmpeg\\" #录播文件存储目录
#</相关位置>#
 #<ffmpeg>#
ffmpeg_location="D:\\Github\\bilibili_auto_live\\bin\\ffmpeg.exe" #ffmpeg.exe 文件位置
ffmpeg_headers_UA="User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36" #headers UA 保证不会403
ffmpeg_headers=' -headers "'+ffmpeg_headers_UA+'"' #headers 保证不会403
ffmpeg_i=' -i "'+live_url+'"' #-i参数
ffmpeg_start=ffmpeg_location+ffmpeg_headers+ffmpeg_i+" -c copy "+recorded_file_storage #总
#主代码
universalCounter = 0
while 1 == 1:
    if universalCounter == 1:
        print("检测到ffmpeg意外关闭/已下播，循环重新开始")
        universalCounter = 0
        time.sleep(30)
    #检测是否开播，如果开播抓取直播源并使用ffmpeg进行录播
    while 1 == 1:
        live_state=requests.post(get_live_inf, get_live_inf_json).json()
        i=live_state['code']
        if i == -412:
            print("IP被拦截，已自动等待10min")
            time.sleep(300)
        live_state=live_state["data"]["live_status"]
        if live_state == 1:
            print("检测到开播 , "+str(time.time()))
            live_url=requests.get(get_live_feeds, get_live_feeds_json).json()
            live_url=live_url["data"]["durl"][0]["url"]
            print("获取到直播源: "+live_url)
            print("ffmpeg已打开，录播开始 , "+str(time.time()))
            random_str=str(int(time.time()))
            recorded_file_storage=recorded_file_storage+random_str+".flv"
            print("ffmprg参数："+ffmpeg_start)
            #os.system(ffmpeg_start)
            os.system('D:\\Github\\bilibili_auto_live\\bin\\ffmpeg -headers "User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36" -i "'+live_url+'" -c copy '+recorded_file_storage)
            universalCounter=1
            break
        time.sleep(30)
    '''
    while 1 == 1:
        if isinstance(proc_exist(''),int):
            time.sleep(5)
        else:
            print("检测到ffmpeg意外关闭 / 已下播，循环重新开始 , "+str(time.time()))
            break
    '''
#备注
'''
os.system()
'''