#import
import json
import os
import sys
import requests
import time

#公共变量
universalCounter=0 #通用计数器
 #<相关信息>#
live_cid="" #直播间房间号
live_platform="web" #直播流格式
#live_quality="4" #画质 2：流畅 3：高墙 4：原画
live_qn="10000" #画质 80：流畅 150：高墙 400：蓝光 10000：原画
live_url="" #直播源url
  #测试源 https://www.natfrp.com/admin/flower.mp4
live_state=""
#</相关信息>#
 #<api_url>#
api_room_status="https://api.live.bilibili.com/room/v1/Room/room_init?id="+live_cid #获取用户直播间状态
#api_get_live_source_quality="http://api.live.bilibili.com/room/v1/Room/playUrl?cid="+live_cid+"&quality="+live_quality+"&platform="+live_platform #解析直播源 画质quality
api_get_live_source_qn="http://api.live.bilibili.com/room/v1/Room/playUrl?cid="+live_cid+"&qn="+live_qn+"&platform="+live_platform #解析直播源 画质qn
'''
api_get_live_source_qn="http://api.live.bilibili.com/room/v1/Room/playUrl"
api_get_live_source_qn_params={
    'cid': live_cid,
    'qn': live_qn,
    'platform': live_platform
}
'''
#</api_url>#
 #<json>#
json_path='' #json文件目录
json_data={} #json更新 用来存储数据
#</json>#

#def
 #<json更新>#
def get_json_data(json_path):
    with open(json_path,'rb') as f:
        params = json.load(f)
        params['sources'][0]["settings"]["input"] = live_url
        #修改内容
        json_data = params
    f.close()
    return json_data
def write_json_data(json_data):
    with open(json_path,'w') as r:
        json.dump(json_data,r)
    r.close()
#</json更新>#

#主代码
while 1==1:
    while 1==1:
        live_state=requests.post(api_room_status).json()
        live_state=live_state["data"]["live_status"]
        if live_state==1:
            live_url=requests.get(api_get_live_source_qn).json()
            live_url=live_url["data"]["durl"][0]["url"]
            print("开播了,当前时间戳"+str(time.time()))
            print("URL: "+live_url)
            the_revised_dict = get_json_data(json_path)
            write_json_data(the_revised_dict)
            print("json文件已修改 , "+str(time.time()))
            #如果备份文件存在，则删除
            if os.path.exists(""):
                os.remove("") 
            os.system('start obs64-1.lnk')
            time.sleep(10)
            os.system('taskkill /f /im obs64.exe')
            os.system('start obs64-1.lnk')
            time.sleep(10)
            os.system('taskkill /f /im obs64.exe')
            os.system('start obs64-1.lnk')
            time.sleep(10)
            os.system('taskkill /f /im obs64.exe')
            os.system('start obs64.exe.lnk')
            print("obs已开启，并自动录屏 , "+str(time.time()))
            break
    while 1==1:
        print("进入循环检测是否下播模式 , "+str(time.time()))
        live_state=requests.post(api_room_status).json()
        live_state=live_state["data"]["live_status"]
        #debug#
        print("测试模式，30s等待开始")
        time.sleep(30)
        live_state=0
        #debug#
        if live_state==0:
            universalCounter=0
            print("检测到疑似下播，开始进行10min的冷却时间 , "+str(time.time()))
            while universalCounter==10:
                live_state=requests.post(api_room_status).json()
                live_state=live_state["data"]["live_status"]
                if live_state==1:
                    print("检测到在冷却时开播，进入校验程序 , "+str(time.time()))
                    break
                time.sleep(60)
                universalCounter=universalCounter+1
                print("这是冷却的第 "+str(universalCounter)+" min , "+str(time.time()))
            if universalCounter==10:
                os.system('taskkill /f /im obs64.exe')
                print("确认已下播，已杀死OBS，并重新开始大循环检测下一场直播 , "+str(time.time()))
                break
            live_state=requests.post(api_room_status).json()
            live_state=live_state["data"]["live_status"]
            if live_state==1:
                print("确认，重新开始大循环，并重新获取直播源 , "+str(time.time()))
                break