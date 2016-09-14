# -*- coding: utf-8 -*-

from urllib.request import urlretrieve, urlopen
from urllib.error import HTTPError,URLError
from bs4 import BeautifulSoup

# 去掉名字中的"/"比如Fate/Zero第二季改为FateZero第二季
def formatName(animeName):
    data=""
    for item in animeName:
        if(item != '/' and item != '!' and item != '?' and item != '"' and item != ":"):
            data=data+item
    return data+".jpg"

def mySpider(anime):
    try:
        html = urlopen(baseUrl + str(anime))
    except HTTPError as e:
        print("error url")
    else:
        bsObj = BeautifulSoup(html)
        image = bsObj.find("div", {"class": "bangumi-preview"}).find("img")
        print("番号："+str(anime))
        # print(formatName(image["alt"]))
        urlretrieve(image["src"], str(anime)+"_"+formatName(image["alt"]))

baseUrl = "http://bangumi.bilibili.com/anime/"

anime = 1
while (anime < 6000):
    mySpider(anime)
    anime = anime + 1

