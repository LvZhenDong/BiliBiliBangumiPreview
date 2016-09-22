# -*-coding:utf-8-*-

from bs4 import BeautifulSoup
import pymysql, re, threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scrapy(driver, uid):
    url = "http://space.bilibili.com/" + str(uid) + "/#!/index"

    driver.get(url)
    if (driver.title == "出错啦! - bilibili.tv"):
        print("error" + str(uid) + " url")
    else:
        try:
            element = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "quantity")))

        finally:
            print(str(uid))
            pageSource = driver.page_source
            bsObj = BeautifulSoup(pageSource)
            name = bsObj.find("span", {"id": "h-name"}).get_text()
            signature = bsObj.find("div", {"class": "h-sign"}).get_text()
            fans = bsObj.find("a", {"href": "#!/fans/fans/1", "class": "item"}).find("span", {
                "class": "quantity"}).get_text()

            fans = getUnit(fans)
            follow = bsObj.find("a", {"href": "#!/fans/follow/1"}).find("span",
                                                                        {
                                                                            "class": "quantity"}).get_text()
            follow = getUnit(follow)

            # sex = bsObj.find("span", {"id": "h-gender"}).attrs['class']
            # print(sex)

            # 获取锁，用于线程同步
            threadLock.acquire()
            cur.execute(
                "INSERT INTO userinfo(name,signature,fans,follow,uid) VALUES (%s,%s,%s,%s,%s)",
                (name, signature, fans, follow, uid))
            conn.commit()
            # 释放锁，开启下一个线程
            threadLock.release()


# 获取数量
def getUnit(count):
    reCount = float(re.match(matchStr, count).group(0))
    unit = count.find("万")
    if (unit != -1):
        reCount = reCount * 10000
    reCount = int(reCount)
    return reCount


class myThread(threading.Thread):
    def __init__(self, uid):
        threading.Thread.__init__(self)
        self.uid = uid

    def run(self):
        driver = webdriver.PhantomJS(
            executable_path='C:/Users/Administrator/Downloads/phantomjs-2.1.1-windows (1)/phantomjs-2.1.1-windows/bin/phantomjs')
        length = self.uid + 900000
        while (self.uid < length):
            scrapy(driver, self.uid)
            self.uid = self.uid + 1
        driver.close()


# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') #改变标准输出的默认编码
matchStr = '[0-9\.]+'

conn = pymysql.connect(host='localhost', port=3306, user='root', db='scraping', charset='utf8')
cur = conn.cursor()

uidBase = 5462
uid1 = 13802
uid2 = 1094840
uid3 = 2013700
uid4 = 3013730
uid5 = 4013748
uid6 = 5002081
uid7 = 6002085
uid8 = 7002086
uid9 = 8000000
uid10 = 9000000
uid11 = 10000000
uid12 = 10100000

uids = [uid1, uid2, uid3, uid4, uid5, uid6, uid7, uid8, uid9, uid10, uid11, uid12]

threadLock = threading.Lock()
threads = []

# 创建子线程
for uid in uids:
    thread = myThread(uid)
    threads.append(thread)

# 开启子线程
for thread in threads:
    thread.start()

# 挂起主线程
for thread in threads:
    thread.join()

cur.close()
conn.close()
