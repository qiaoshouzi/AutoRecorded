import json
import os
import sys
import requests
import time

live_cid="" #直播间房间号
live_platform="web" #直播流格式
#live_quality="4" #画质 2：流畅 3：高墙 4：原画
live_qn="10000" #画质 80：流畅 150：高墙 400：蓝光 10000：原画

api_get_live_source_qn="http://api.live.bilibili.com/room/v1/Room/playUrl?cid="+live_cid+"&qn="+live_qn+"&platform="+live_platform #解析直播源 画质qn
live_url=requests.get(api_get_live_source_qn).json()
print(live_url)
#live_url=live_url["data"]["durl"][0]["url"]