#-*-coding:utf-8-*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from urllib.error import HTTPError
import time

login_url='https://passport.bilibili.com/ajax/miniLogin/minilogin'
home_url='http://www.bilibili.com'
chrome_driver_path=r'C:/Users/Administrator/AppData/Local/Programs/Python/Python35/chromedriver.exe'

account='15594879056'
password='740049121'

# 观看视频
def watch_video(driver):
    driver.get(home_url)
    try:
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "v-item")))
    except:
        print('open hoem error')
    else:
        html=driver.page_source
        bsObj=BeautifulSoup(html)
        av=bsObj.find('div',{"class":"v-item"}).find('a')['href']
        av_url=home_url+av
        driver.get(av_url)
        try:
            WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "t-right-top")))
        except:
            print('watch video error')
        else:
            print("av_url:"+av_url)
            time.sleep(30)
            coin(driver)
            time.sleep(10)
            share(driver)
            time.sleep(30)
# 分享
def share(driver):
    # driver.find_elements_by_class_name('t-right-top')[0].click()
    driver.get('')
    pass

# 投硬币
def coin(driver):
    driver.find_elements_by_class_name('t-right-top')[3].click()
    time.sleep(20)
    # 投一枚硬币
    coin_one=driver.find_element_by_class_name('coin-nav-single')
    coin_one.click()
    btn=driver.find_element_by_class_name('btnbox').find_element_by_class_name('ok')
    # btn.click()
    print("coin click")


# 开始一天的工作,登录
def login():
    driver=webdriver.Chrome(chrome_driver_path)
    driver.get(login_url)
    # 登录
    driver.find_element_by_id('login-username').send_keys(account)
    driver.find_element_by_id('login-passwd').send_keys(password)
    driver.find_element_by_id('login-submit').click()

    try:
        WebDriverWait(driver,100).until(EC.title_is(u'Bilibili ~ Cheer！'))
    except:
        print('login error')
        driver.close()
    else:
        watch_video(driver)
        driver.close()

while True:
    login()
    time.sleep(86300)





