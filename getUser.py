# -*-coding:utf-8-*-

from urllib.request import urlretrieve, urlopen
from urllib.error import HTTPError, URLError

from bs4 import BeautifulSoup
import pymysql, re, threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrapy(driver, uid):
    url = "http://space.bilibili.com/" + str(uid) + "/#!/index"
    try:
        html = urlopen(url)
    except HTTPError as e:
        print("error"+str(uid)+" url")
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

            fans = getUnit(fans)
            # print(fans)
            follow = bsObj.find("a", {"href": "#!/fans/follow/1"}).find("span",
                                                                        {
                                                                            "class": "quantity"}).get_text()
            follow = getUnit(follow)
            # print(follow)
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
        length = self.uid + 1000000
        while (self.uid < length):
            scrapy(driver, self.uid)
            self.uid = self.uid + 1
        driver.close()


# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') #改变标准输出的默认编码
matchStr = '[0-9\.]+'

conn = pymysql.connect(host='localhost', port=3306, user='root', db='scraping', charset='utf8')
cur = conn.cursor()

uid1 = 5462
uid2 = uid1 + 1000000
uid3 = uid2 + 1000000
uid4 = uid3 + 1000000
uid5 = uid4 + 1000000

threadLock = threading.Lock()

thread1=myThread(uid1)
thread2=myThread(uid2)
thread3=myThread(uid3)
thread4=myThread(uid4)
thread5=myThread(uid5)

thread1.start()
thread2.start()
thread3.start()
thread4.start()
thread5.start()

thread1.join()
thread2.join()
thread3.join()
thread4.join()
thread5.join()

cur.close()
conn.close()



