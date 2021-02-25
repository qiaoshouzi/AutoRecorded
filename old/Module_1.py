#Module_1 模块一#
#抓取直播源URL并修改json文件#

#import
import json
import os
import sys
import requests
import time

#公共变量
 #<相关信息>#
live_cid="870004" #直播间房间号
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
#</api_url>#
 #<json>#
json_path='C:\\Users\\\\AppData\\Roaming\\obs-studio\\basic\\scenes\\main.json' #json文件目录
json_data={} #json更新 用来存储数据
#</json>#

#def
 #<json更新>#
def get_json_data(json_path):
    with open(json_path,'rb') as f:
        params = json.load(f)
        params['sources'][1]["settings"]["input"] = live_url
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
print("开始 , "+str(time.time()))
live_url=requests.get(api_get_live_source_qn).json()
live_url=live_url["data"]["durl"][0]["url"]
print("URL: "+live_url)
the_revised_dict = get_json_data(json_path)
write_json_data(the_revised_dict)
print("json文件已修改 , "+str(time.time()))