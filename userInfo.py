# -*- coding: utf-8 -*-

from urllib.request import urlretrieve, urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
import pymysql, re

conn = pymysql.connect(host='localhost', port=3306, user='root', db='scraping',charset='utf8')

cur = conn.cursor()

url = 'http://bangumi.bilibili.com/anime/'
matchStr = '[0-9\.]+'


def getInfo(index):
    print("index:"+str(index))
    try:
        html = urlopen(url + str(index))
    except HTTPError as e:
        print("error url")
    else:
        bsObj = BeautifulSoup(html)
        # 番剧名
        name = bsObj.find("h1", {"class": "info-title"}).get_text()
        # print(name)
        # 总播放
        play = bsObj.find("span", {"class": "info-count-item info-count-item-play"}).em.get_text()
        playCount = getUnit(play)
        # 追番人数
        fans = bsObj.find("span", {"class": "info-count-item info-count-item-fans"}).em.get_text()
        fansCount = getUnit(fans)
        # 弹幕总数
        review = bsObj.find("span",
                            {"class": "info-count-item info-count-item-review"}).em.get_text()
        reviewCount = getUnit(review)
        # 简介
        introduction = bsObj.find("div", {"class": "info-desc"}).get_text()
        # print(introduction)

        cur.execute(
            "INSERT INTO bangumi(animeId,name,play,fans,review,introduction) VALUES (%s,%s,%s,%s,%s,%s)",
            (index,name,playCount,fansCount,reviewCount,introduction))
        conn.commit()


# 获得数量\
def getUnit(count):
    reCount = float(re.match(matchStr, count).group(0))
    unit = count.find("万")
    if (unit != -1):
        reCount = reCount * 10000
    reCount = int(reCount)
    # print(str(reCount))
    return reCount

animeId=1668
while(animeId < 6000):
    getInfo(animeId)
    animeId = animeId + 1

cur.close()
conn.close()
