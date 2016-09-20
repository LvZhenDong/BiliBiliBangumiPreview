# -*-coding:utf-8-*-

from urllib.request import urlretrieve, urlopen
from urllib.error import HTTPError, URLError

from bs4 import BeautifulSoup
import pymysql, re, time, sys, io
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') #改变标准输出的默认编码
matchStr = '[0-9\.]+'


def scrapy(driver, uid):
    url="http://space.bilibili.com/" + str(uid) + "/#!/index"
    try:
        html=urlopen(url)
    except HTTPError as e:
        print("error url")
    else:
        driver.get(url)
        try:
            element = WebDriverWait(driver, 200).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "quantity")))

        finally:
            print(str(uid))
            pageSource = driver.page_source
            bsObj = BeautifulSoup(pageSource)
            name = bsObj.find("span", {"id": "h-name"}).get_text()
            # print(name)
            signature = bsObj.find("div", {"class": "h-sign"}).get_text()
            # print(signature)
            fans = bsObj.find("a", {"href": "#!/fans/fans/1", "class": "item"}).find("span", {
                "class": "quantity"}).get_text()

            fans=getUnit(fans)
            # print(fans)
            follow = bsObj.find("a", {"href": "#!/fans/follow/1"}).find("span",
                                                                        {
                                                                            "class": "quantity"}).get_text()
            follow=getUnit(follow)
            # print(follow)
            # sex = bsObj.find("span", {"id": "h-gender"}).attrs['class']
            # print(sex)

        cur.execute(
            "INSERT INTO userinfo(name,signature,fans,follow,uid) VALUES (%s,%s,%s,%s,%s)",
            (name,signature,fans,follow,uid))
        conn.commit()


# 获取数量
def getUnit(count):
    reCount = float(re.match(matchStr, count).group(0))
    unit = count.find("万")
    if (unit != -1):
        reCount = reCount * 10000
    reCount = int(reCount)
    return reCount


conn = pymysql.connect(host='localhost', port=3306, user='root', db='scraping', charset='utf8')
cur = conn.cursor()

driver = webdriver.PhantomJS(
    executable_path='C:/Users/Administrator/Downloads/phantomjs-2.1.1-windows (1)/phantomjs-2.1.1-windows/bin/phantomjs')

uid = 1
while (True):
    scrapy(driver, uid)
    uid = uid + 1

driver.close()
cur.close()
conn.close()
