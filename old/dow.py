import json
import os
import sys
import requests
import time
from clint.textui import progress

file_flv="D:\\OBS录像\\file_flv\\ying_treasure.flv"
live_url="https://d1--cn-gotcha03.bilivideo.com/live-bvc/920432/live_21374533_1880543.flv?cdn=cn-gotcha03&expires=1614096552&len=0&oi=1901843014&pt=web&qn=10000&trid=389954389432487da5becfd34a176783&sigparams=cdn,expires,len,oi,pt,qn,trid&sign=1647a4e1493b763fd51ea1a9998f75ba&ptype=0&src=5&sl=2&order=4"

if os.path.exists(file_flv):
    os.remove(file_flv) 
file_flv_flv=requests.get(live_url, stream=True)
with open(file_flv,'wb') as Pypdf:
    total_length=int(file_flv_flv.headers.get('content-length'))
    for ch in progress.bar(file_flv_flv.iter_content(chunk_size=2391975), expected_size=(total_length/1024) +1):
        if ch:
            Pypdf.write(ch)
print("flv文件下载完成 , "+str(time.time()))