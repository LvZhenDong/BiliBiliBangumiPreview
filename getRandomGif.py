# -*-coding:utf-8-*-

from urllib.request import urlopen, urlretrieve
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re




# 去掉名字中的"/"比如Fate/Zero第二季改为FateZero第二季
def formatName(animeName):
    data = ""
    for item in animeName:
        if (item != '/' and item != '!' and item != '?' and item != '"' and item != ":"):
            data = data + item
    return data + ".gif"


def getGif(driver,noChange):
    driver.get('http://www.bilibili.com/')
    try:
        element = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "random-p-movie")))
    except:
        print('open error')
    else:
        html = driver.page_source
        bsObj = BeautifulSoup(html)
        gif = bsObj.find("div", {"class": "random-p-movie"}).find("img")
        name = formatName(gif['alt'])
        if gif['alt'] not in gifs:
            # 新的gif
            urlretrieve(gif['src'], filename='./gifs/' + name)
            gifs.add(gif['alt'])
            print(name)
            noChange = 0
        else:
            noChange = noChange + 1

    return noChange

gifs = set()
noChange = 0

driver = webdriver.PhantomJS(
    executable_path='E:/workspace-python/phantomjs-2.1.1-windows/bin/phantomjs')
while(noChange < 5000):
    noChange=getGif(driver,noChange)
    print(str(noChange))
print("noChange")
