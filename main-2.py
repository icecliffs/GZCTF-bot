# 
# @rYu1nser Digital Watermarking
# @Author: rYu1nser
# @Date: 2022/11/11
#
import asyncio
import requests
import json,time
from datetime import datetime

URL = "https://ctfer.club"
GROUP_NOTICE_ID = 731400372
#GROUP_NOTICE_ID = 280853253
GROUP_EVENTS_ID = 280853253

dic = {
    'platform-notice': URL + '/api/game/1/notices',
    'platform-events': URL + '/api/game/3/events?hideContainer=false&count=2&skip=0'
}

def processTime(t):
    t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    return t

def getNotice():
    request = requests.session()
    try:
        res = request.get(dic['platform-notice'])
    except:
        return []
    t = json.loads(res.text)
    return t

async def sendMessageNotice():
    global noticeList, noticeLen
    while True:
        try:
            request = requests.session()
            tmpList = getNotice()
            tmpListLen = tmpList[len(tmpList)-1]['id']
            print(noticeLen, tmpListLen)
            print('[*] 等待数据接入！（公告检查）')
            if (tmpList == 0):
                print('[*] 异步暂停，请查看程序！（公告检查）')
                await asyncio.sleep(3)
                continue
            if (noticeLen < tmpListLen):
                print('[*] 装载数据（公告检查）')
                message = ""
                t = tmpListLen - noticeLen
                if (t > 1):
                    for i in range(0, t):
                        if (tmpList[i]['type'] == 'Normal'):
                            timeA = processTime(tmpList[i]['time'])
                            print(tmpList[i]['content'])
                            message += timeA + '\n' + '【公告】' + str(tmpList[i]['content']) + '\n'
                        elif (tmpList[i]['type'] == 'FirstBlood'):
                            timeA = processTime(tmpList[i]['time'])
                            print(tmpList[i]['content'])
                            message += timeA + '\n' + '【一血】' + str(tmpList[i]['content']) + '\n'
                        elif (tmpList[i]['type'] == 'SecondBlood'):
                            timeA = processTime(tmpList[i]['time'])
                            print(tmpList[i]['content'])
                            message += timeA + '\n' + '【二血】' + str(tmpList[i]['content']) + '\n'
                        elif (tmpList[i]['type'] == 'ThirdBlood'):
                            timeA = processTime(tmpList[i]['time'])
                            print(tmpList[i]['content'])
                            message += timeA + '\n' + '【三血】' + str(tmpList[i]['content']) + '\n'
                        elif (tmpList[i]['type'] == 'NewHint'):
                            timeA = processTime(tmpList[i]['time'])
                            print(tmpList[i]['content'])
                            message += timeA + '\n' + '【提示】' + str(tmpList[i]['content']) + '\n'
                        elif (tmpList[i]['type'] == 'NewChallenge'):
                            timeA = processTime(tmpList[i]['time'])
                            print(tmpList[i]['content'])
                            message += timeA + '\n' + '【上题目啦】' + str(tmpList[i]['content']) + '\n'
                    print('[*] 状态成功，发送下列数据！')
                    print(message)
                    r = request.get("http://127.0.0.1:8080/send_group_msg?group_id="
                                    + str(GROUP_NOTICE_ID) +
                                    "&message=" + str(message))
                    noticeLen = tmpListLen
                    noticeList = tmpList
                else:
                    for i in range(0, t):
                        if (tmpList[i]['type'] == 'Normal'):
                            timeA = processTime(tmpList[i]['time'])
                            print(tmpList[i]['content'])
                            message += timeA + '\n' + '【公告】' + str(tmpList[i]['content'])
                        elif (tmpList[i]['type'] == 'FirstBlood'):
                            timeA = processTime(tmpList[i]['time'])
                            print(tmpList[i]['content'])
                            message += timeA + '\n' + '【一血】' + str(tmpList[i]['content'])
                        elif (tmpList[i]['type'] == 'SecondBlood'):
                            timeA = processTime(tmpList[i]['time'])
                            print(tmpList[i]['content'])
                            message += timeA + '\n' + '【二血】' + str(tmpList[i]['content'])
                        elif (tmpList[i]['type'] == 'ThirdBlood'):
                            timeA = processTime(tmpList[i]['time'])
                            print(tmpList[i]['content'])
                            message += timeA + '\n' + '【三血】' + str(tmpList[i]['content'])
                        elif (tmpList[i]['type'] == 'NewHint'):
                            timeA = processTime(tmpList[i]['time'])
                            print(tmpList[i]['content'])
                            message += timeA + '\n' + '【提示】' + str(tmpList[i]['content'])
                        elif (tmpList[i]['type'] == 'NewChallenge'):
                            timeA = processTime(tmpList[i]['time'])
                            print(tmpList[i]['content'])
                            message += timeA + '\n' + '【上题目啦】' + str(tmpList[i]['content'])
                    print('[*] 状态成功，发送下列数据！')
                    print(message)
                    r = request.get("http://127.0.0.1:8080/send_group_msg?group_id="
                                    + str(GROUP_NOTICE_ID) +
                                    "&message=" + str(message))
                    noticeLen = tmpListLen
                    noticeList = tmpList
            else:
                noticeLen = tmpListLen
                noticeList = tmpList
            await asyncio.sleep(3)
        except Exception as e:
            print(e,'[!] 程序出错！可能是 120条/m 限制（公告检查）')
            continue
if __name__ == "__main__":
    noticeList = getNotice()
    noticeLen = (noticeList[len(noticeList)-1]['id'])
    # eventsList = getEvents()
    # eventsLen = len(eventsList)
    loop = asyncio.get_event_loop()
    # tasks = [sendMessageNotice(),sendMessageEvents()]
    tasks = [sendMessageNotice()]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
