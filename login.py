# -*-coding:utf-8-*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def follow(driver,uid):

    driver.get('http://space.bilibili.com/'+str(uid)+'/#!/index')
    if (driver.title == "出错啦! - bilibili.tv"):
        print("error" + str(uid) + " url")
    else:
        try:
            element = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "quantity")))
        except:
            print('follow error')
        else:
            print('CLICK')
            driver.find_element_by_css_selector("*[class^='h-f-btn h-follow']").click()
            print('AFTER FOLLOW')


# ------------------------------

# driver = webdriver.PhantomJS(
#     executable_path='E:/workspace-python/phantomjs-2.1.1-windows/bin/phantomjs')
driver=webdriver.Chrome(r"C:/Users/Administrator/AppData/Local/Programs/Python/Python35/chromedriver.exe")

driver.get('https://passport.bilibili.com/ajax/miniLogin/minilogin')

# 账号
username = 'username'
# 密码
password = '******'
driver.find_element_by_id('login-username').send_keys(username)
driver.find_element_by_id('login-passwd').send_keys(password)
print('CLICK')
driver.find_element_by_id('login-submit').click()
print('AFTER LOGIN')
try:
    element=WebDriverWait(driver,20).until(EC.title_is(u'Bilibili ~ Cheer！'))
except:
    print('login error')
else:
    uid = 34
    while(True):
        print('uid:'+str(uid))
        follow(driver,uid)
        uid += 1

