import requests
from bs4 import BeautifulSoup
import json
import random

#Core Page
#https://api.vc.bilibili.com/dynamic_repost/v1/dynamic_repost/repost_detail?dynamic_id=265215506136622321

#获取单页的转发列表（20个）
#返回列表：[0]是return code，[1]是获取到的列表
def GetOnePage(url):
    resList = []

    response = requests.get(url)
    resJson = json.loads(response.text)

    #Return code, return 0 if reposters exist
    rescode = resJson['code']
    
    if rescode == 0:
        #获取所单页的转发元素
        items = resJson['data']['items']
        for item in items:
            itemJson = json.loads(item['card'])
            #定位到UID
            resList.append(itemJson['user']['uid'])
    
    return [rescode, resList]

def GetPagesCycle(url):
    allUIDSet = []

    #获取第一页
    firstPageGet = GetOnePage(url)
    retCode = firstPageGet[0]
    allUIDSet += firstPageGet[1]

    offsetIndex = 20
    while retCode == 0:
        #偏移量增加，生成下一页的url
        offsetUrl = url + '&offset=1:' + str(offsetIndex)
        currentPage = GetOnePage(offsetUrl)
        retCode = currentPage[0]
        allUIDSet += currentPage[1]

        offsetIndex += 20
    
    return allUIDSet

#随机方法，传入UID列表
def GetOneLuckyDog(uidList):
    listSize = len(uidList)
    luckyNum = random.randint(0, listSize - 1)
    return uidList[luckyNum]

print('Bilibili转发抽奖工具v1.0')
print('Bilibili@鱼丸子_Official')

url = 'https://api.vc.bilibili.com/dynamic_repost/v1/dynamic_repost/repost_detail?dynamic_id=' + input('输入动态号')
repostList = list(dict.fromkeys(GetPagesCycle(url)))
print('成功获取转发列表')
generateNum = int(input('输入随机数量'))

print('获取到的用户')
for i in range(0, generateNum):
    uidGet = GetOneLuckyDog(repostList)
    userPageUrl = 'https://space.bilibili.com/' + str(uidGet)
    print(userPageUrl)

input()