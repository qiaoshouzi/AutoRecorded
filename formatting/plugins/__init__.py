from .serverChan import serverChan
from .qqAPI import qqGroup

def plug_serverChan_push(ftqq_SendKey, ftqq_title):
    serverChan.push(ftqq_SendKey, ftqq_title)
def plug_qqAPI_groupPush(ftqq_SendKey):
    qqGroup.push(ftqq_SendKey)