# -*- coding:utf-8 -*-
import time
# ブラウザを操作するのに必要なモジュール
from selenium import webdriver
# スクリプトを起動し続けるかつ定期実行するために必要なモジュール
import schedule
# IPアドレスを取得するのに必要なモジュール
import socket
import fcntl
import struct
# 現在時刻を表示するのに必要なモジュール
import datetime
# 使用しているプラットフォームを表示するのに必要なモジュール
import platform
import os

print("実行開始")
print(datetime.datetime.now())

def ip_print():
  host_name = socket.gethostname()

  if platform.system() == "Linux":
    ipaddress = os.popen('ip addr show wls3').read().split("inet ")[1].split("/")[0]

  else:
    ipaddress = socket.gethostbyname(host_name)

  print("ホスト名 : " + host_name)
  print("IPアドレス : " + ipaddress)


ip_print()

def login():

    print("login session : ")
    print(datetime.datetime.now())
    print(ip_print())
    #カレントディレクトリにchromedriverがある前提
    driver = webdriver.Chrome()

    try:
      #usernameをのところに自分の学籍番号
      u_text = "315156p"
      #passwordのところに自分のパスワード
      p_text = "t"

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


      print("ログインセイコウ")
      
    except:
      print("ログインシッパイ")
      
    ip_print()
    time.sleep(10)
    driver.close()


def logout():
    print(ip_print())

    print("logout session : ")
    print(datetime.datetime.now())
    driver = webdriver.Chrome()
    
    try:
      driver.get("https://captive-portal/cp/logout")
      time.sleep(1)
      SubmitButton = driver.find_element_by_name("cpSubmit")
      SubmitButton.click()
      print("ログアウトセイコウ")

    
    except:
      print("ログアウトシッパイ")

    ip_print()
    time.sleep(3)
    driver.close()

schedule.every().day.at("15:44").do(logout)

schedule.every().day.at("15:45").do(login)


while True:
  schedule.run_pending()
  time.sleep(1)
