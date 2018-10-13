# -*- coding:utf-8 -*-
import time
from selenium import webdriver
#カレントディレクトリにchromedriverがある前提
driver = webdriver.Chrome("./chromedriver")

#usernameをのところに自分の学籍番号
u_text = "username"
#passwordのところに自分のパスワード
p_text = "password"

driver.get("https://captive-portal/cp/content/cpLogin.html")

time.sleep(1)

# ユーザID
Username = driver.find_element_by_css_selector("#userId")
Username.send_keys(u_text)

time.sleep(1)
# パスワード
Password = driver.find_element_by_css_selector("#userPass")
Password.send_keys(p_text)

time.sleep(1)

PolicyCheck = driver.find_element_by_css_selector("#policyCheck")
PolicyCheck.click()

time.sleep(1)

SubmitButton = driver.find_element_by_css_selector("#submitButton")
SubmitButton.click()
SubmitButton.submit()

time.sleep(20)
driver.close()
