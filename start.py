#import
import os
import sys
import time
import json
import requests
import random
import logging
import logging.handlers

#���ܿ���
switch_ftqq=False #�Ƿ����������� ���������һ��Ҫ��д ftqq_SendKey ������ܻᱨ��
switch_qqGroup=False #�Ƿ���QQȺ���� ���������һ��Ҫ��д qqGroup_id qqGroup_API ������ܻᱨ��

#����
universalCounter=0 #ͨ�ü�����

live_cid="" #ֱ���䷿��� #����
live_platform="web" #ֱ������ʽ #ѡ��
live_quality="4" #���� 2������ 3����ǽ 4��ԭ�� #ѡ��
live_qn="10000" #���� 80������ 150����ǽ 400������ 10000��ԭ�� #ѡ��
live_url="" #ֱ��Դurl
live_state="" #ֱ����״̬�� 0 1

api_get_live_feeds="http://api.live.bilibili.com/room/v1/Room/playUrl" #��ȡ ֱ��ԴURL ��API
api_get_live_feeds_json={
    'cid': live_cid,
    'qn': live_qn,
    #'quality': live_quality,
    'platform': live_platform
}
api_post_live_inf="https://api.live.bilibili.com/room/v1/Room/room_init" #��ȡ ֱ������Ϣ ��API
api_post_live_inf_json={
    'id': live_cid
}

recordingFolder="" #¼���ļ��洢Ŀ¼ #����

ffmpeg_location="" #ffmpeg.exe �ļ�λ��  #����
ffmpeg_UA="User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36" #headers UA ��֤����403 #ѡ��

ftqq_SendKey="" #���ǵ�SendKey #����
ftqq_returnValue="" #����ֵ
ftqq_code="" #״̬��Ϣ
ftqq_info="" #������Ϣ
ftqq_title="" #������Ϣ��title
ftqq_pushid="" #�������
ftqq_readkey="" #�������
ftqq_check_returnValue="" #���_����ֵ
ftqq_check_code=0 #���_code
ftqq_check_data="" #���_data��Ϣ
ftqq_check_message="" #���_������Ϣ3
ftqq_check_readkey="" #���_���

qqGroup_id="" #Ҫ���͵�QQȺ�� #����
qqGroup_message="" #Ҫ���͵���Ϣ
qqGroup_API="" #API��ַ #����
qqGroup_API_json={
    'group_id': qqGroup_id,
    'message': qqGroup_message
}

#��ʼ��
 #��־��ʼ��
  #��ʼ��
logging.basicConfig(level = logging.INFO,format = '%(lineno)d | %(asctime)s - %(name)s - %(levelname)s - %(message)s') #���ÿ���̨��ʾlog����ʽ
  #����
logger = logging.getLogger("AutoRecorded")
  #����handler
handler1 = logging.FileHandler("logs\\log-"+str(int(time.time()))+".log") #����log�ļ�����ʽ
handler1.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s|%(name)-12s+ %(levelname)-8s++%(message)s') #���� log�ļ� ��ʾlog����ʽ
handler1.setFormatter(formatter)
handler2 = logging.StreamHandler()
handler2.setLevel(logging.ERROR)
logger.addHandler(handler1)
logger.addHandler(handler2)

#def
 #��������
def ftqqTurbo(ftqq_SendKey, ftqq_title):
    if switch_ftqq==True:
        ftqq_returnValue=requests.post("https://sctapi.ftqq.com/"+ftqq_SendKey+".send?title="+ftqq_title).json()
        ftqq_code=ftqq_returnValue["code"]
        ftqq_pushid=ftqq_returnValue["data"]["pushid"]
        ftqq_readkey=ftqq_returnValue["data"]["readkey"]
        if ftqq_code == 0:
            logger.info(" [��������] ���ͳɹ�")
            logger.info("pushid="+ftqq_pushid+"  readkey="+ftqq_readkey)
            '''#�������δ֪BUG������
            while 1==1:
                ftqq_check_returnValue=requests.post("https://sctapi.ftqq.com/push?id="+ftqq_pushid+"&readkey="+ftqq_readkey).json()
                ftqq_check_code=ftqq_check_returnValue["code"]
                ftqq_check_message=ftqq_check_returnValue["message"]
                ftqq_check_data=ftqq_check_returnValue["data"]
                if ftqq_check_code == 10001:
                    logger.error(" [�������͸���] ����10001 ������Ϣ: "+ftqq_check_message)
                    break
                else:
                    if ftqq_check_data == None:
                        logger.error(" [�������͸���] data�հף�����pushid/readkey��������")
                        break
                    else:
                        if ftqq_check_readkey["readkey"] == ftqq_readkey:
                            logger.info(" [�������͸���] ���ͳɹ�")
                            break
                        else:
                            logger.error(" [�������͸���] δ֪���󣬷���ֵ: "+ftqq_check_returnValue)
                            break
            '''
        if ftqq_code == 40001:
            ftqq_info=ftqq_returnValue["info"]
            logger.error(ftqq_info)
        if ftqq_code == 20001:
            ftqq_info=ftqq_returnValue["info"]
            logger.error(ftqq_info)
    else:
        logger.info(" [��������] δ�����������͹��ܣ�����ʧ��")

 #QQȺ����
def qqGroupPush(qqGroup_id, qqGroup_message):
    if switch_qqGroup == True:
        qqGroup_API_json={
        'group_id': qqGroup_id,
        'message': qqGroup_message
        }
        qqGroup_code=requests.post(qqGroup_API, qqGroup_API_json)
        if qqGroup_code["retcode"] == 100:
            logger.error(" [QQȺ����] QQȺ���ʹ���")
            ftqqTurbo(ftqq_SendKey, "[QQȺ����] [Error] QQȺ���ʹ���")
    else:
        logger.info(" [QQȺ����] δ����QQȺ���͹��ܣ�����ʧ��")

#������
universalCounter = 0 #��������0
logger.info(" [BOT] ��ʼ����")
while 1 == 1:
    #��������� == 1������ffmpeg�ѹرգ����log���ȴ�30s����ȴ��
    if universalCounter == 1:
        logger.info(" [����] ��⵽ffmpeg����ر�/���²���ѭ�����¿�ʼ")
        ftqqTurbo(ftqq_SendKey, "[����] ��⵽ffmpeg����ر�/���²���ѭ�����¿�ʼ")
        qqGroupPush(qqGroup_id, "��⵽�²����п��ܲ�׼ȷ��")
        universalCounter = 0
        time.sleep(30)
    #����Ƿ񿪲����������ץȡֱ��Դ��ʹ��ffmpeg����¼��
    while 1 == 1:
        live_state=requests.post(api_post_live_inf, api_post_live_inf_json).json() #��ȡֱ����ϸ json
        i=live_state['code']
        if i == -412: #����Ƿ�IP��ʱBAN����ȴ5min
            logger.error(" [����] IP�����أ����Զ��ȴ�5min")
            ftqqTurbo(ftqq_SendKey, "[����] IP�����أ����Զ��ȴ�5min")
            time.sleep(300)
        live_state=live_state["data"]["live_status"] #��ȡֱ����״̬�� 0 δ���� 1 ����
        if live_state == 1:
            logger.info(" [BOT] ��⵽����")
            ftqqTurbo(ftqq_SendKey, "[BOT] ��⵽����")
            qqGroupPush(qqGroup_id, "��⵽�������п��ܲ�׼ȷ��")
            live_url = requests.get(api_get_live_feeds, api_get_live_feeds_json).json() #��ȡֱ��ԴURL json
            live_url = live_url["data"]["durl"][0]["url"] #��ȡֱ��ԴURL
            logger.info(" [BOT] ��ȡ��ֱ��Դ: "+live_url)
            logger.info(" [BOT] ffmpeg�Ѵ򿪣�¼����ʼ")
            file_name = str(int(time.time())) #����ǰʱ�������Ϊ¼���ļ���
            recordingFolder = recordingFolder+file_name+".flv"
            os.system(ffmpeg_location+' -headers "'+ffmpeg_UA+'" -i "'+live_url+'" -c copy '+recordingFolder)
            universalCounter = 1 #������������Ϊ1ȷ����ʶ��
            break
        time.sleep(30)