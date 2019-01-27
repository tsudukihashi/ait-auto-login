# -*- coding:utf-8 -*-
import os
import pickle
import socket
import time
import tkinter as tk
import re
from tkinter import *
from tkinter import ttk
from selenium import webdriver

root = tk.Tk()
root.title("Ashikaga University Auto Login")
root.geometry("480x320")


host_name = socket.gethostname()
ipaddress = socket.gethostbyname(host_name)
ipaddress_all = socket.gethostbyname_ex(host_name)



def ip_get():
  global host_name,ipaddress,ipaddress_all
  host_name = socket.gethostname()
  ipaddress = socket.gethostbyname(host_name)
  ipaddress_all = socket.gethostbyname_ex(host_name)

  IP_Address["text"] = "現在のIPアドレス:      " + ipaddress
  


#セーブしたかどうか
isSave = False

#エントリーに入力された文字列を取得し保存の関数を呼び出す
def save_btn():
  global isSave
  username_text = Username.get()
  password_text = Password.get()

  if len(username_text) > 0 and len(password_text) > 0:
    save(username_text, "username")
    save(password_text, "password")

    isSave = True

    u_text = read("username")
    p_text = read("password")
  else:
    print("セーブに必要なデータが不足しています")
    Status["text"] = "学籍番号とパスワードを入力してください．"

#保存
def save(text,name):
  with open(name + '.pickle', mode='wb') as f:
    pickle.dump(text,f)

#読み込み
def read(name):
  try:
    with open(name + '.pickle', mode='rb') as f:
      text = pickle.load(f)
  except:
    text = ""
    global isSave
    isSave = False
  return text

#削除
def delete_data():
  global isSave 
  isSave = False
  try:
    os.remove("./username.pickle")
    os.remove("./password.pickle")
    Password.delete(0, tk.END)
    Username.delete(0, tk.END)

    Status["text"] = "削除しました．"
  except:
    print("delete済")
    Status["text"] = "削除済です．"

u_text = read("username")
p_text = read("password")

if len(u_text) > 0 and len(p_text) > 0:
  isSave = True
else:
  isSave = False

def all_ip_show():
  sub2win = Toplevel()
  message = ipaddress_all
  sub2win.geometry("400x200")
  msg = tk.Label(sub2win, text=message)
  msg.pack()

def readme_btn():
  subwin = Toplevel()
  message ="""
  
  足利大学の非公式ツールです．
  ログインを自動化します．
  学籍番号とパスワードを入力した後
  セーブを押してからログインしてください
  セーブでデータを保持します．
  データを削除では保存されたデータごと消します．

  消した後
  再度入力し，セーブしてからログインを実行してください．
  """
  subwin.geometry("400x200")
  msg = tk.Label(subwin, text=message)
  msg.pack()


#login
def login():
  u_text = read("username")
  p_text = read("password")
  global isSave

  if len(u_text) > 0 and len(p_text) > 0:
    isSave = True
  else:
    isSave = False

  if isSave == False:
    print("ログインするための情報がありません")
    Status["text"] = "ログインするための情報がありません．"

  elif isSave == True:
    if os.name == "posix":
      driver = webdriver.Chrome("./chromedriver")
    elif os.name == "nt":
      driver = webdriver.Chrome("./chromedriver.exe")
    
    driver.get("https://captive-portal/cp/content/cpLogin.html")
    time.sleep(1)

    try:

      #ユーザID
      Username = driver.find_element_by_css_selector("#userId")
      Username.send_keys(u_text)

      time.sleep(1)
      #パスワード
      Password = driver.find_element_by_css_selector("#userPass")
      Password.send_keys(p_text)

      time.sleep(1)
      PolicyCheck = driver.find_element_by_css_selector("#policyCheck")
      PolicyCheck.click()
      time.sleep(1)
      SubmitButton = driver.find_element_by_css_selector("#submitButton")
      SubmitButton.click()
      SubmitButton.submit()

      Login.state(["disabled"])
      time.sleep(20)

    #例外処理すでにログイン済もしくは学内LANにアクセスできない場合
    except:
      Status["text"] = "すでにログインしているか，学内LANにアクセスできません．"
      time.sleep(2)
      

    driver.close()

def logout():
    if os.name == "posix":
      driver = webdriver.Chrome("./chromedriver")
    elif os.name == "nt":
      driver = webdriver.Chrome("./chromedriver.exe")

    try:
      driver.get("https://captive-portal/cp/logout")
      time.sleep(1)
      SubmitButton = driver.find_element_by_name("cpSubmit")
      SubmitButton.click()

    except:
      Status["text"] = "ログアウトに失敗しました．学内LANに接続していません．"
    
    time.sleep(3)
    driver.close()

title = tk.Label(text="足利大学 非公式ツール", font=("", 20))
title.pack()

label = tk.Label(text="学籍番号とパスワードを入力してください")
label.pack()

#Username
frame1 = tk.Frame(root, pady=10)
frame1.pack()
name = tk.Label(frame1,text="学籍番号")
name.pack(side="left")

Username = tk.Entry(frame1)
Username.insert(tk.END,u_text)
Username.pack(side="left")

#Password
frame2 = tk.Frame(root, pady=10)
frame2.pack()
password = tk.Label(frame2,text="       パスワード")
password.pack(side="left")

Password = tk.Entry(frame2)
Password["show"] = "*"
Password.insert(tk.END,p_text)
Password.pack(side="left")

#password表示
isShow = False

def ShowSwitch():
  global isShow
  isShow = not(isShow)

  if isShow == True:
    Password["show"] = ""
    Status["text"] = "パスワードを表示しています．"
  else:
    Password["show"] = "*"
    Status["text"] = "パスワードを隠しています．"



Show = tk.Button(frame2, text="目",command=ShowSwitch)
Show.pack(side="left")

frame3 = tk.Frame(root, pady=10)
frame3.pack()

HOST_NAME =  tk.Label(frame3,text="ホスト名:" + host_name)
HOST_NAME.pack()

IP_Address = tk.Label(frame3, text="現在のIPアドレス:      " + ipaddress)
IP_Address.pack()

Update_Btn = tk.Button(frame3, text="更新",command=ip_get)
Update_Btn.pack()

Status = tk.Label(text="")
Status.pack(side="top")

Menuvar = Menu(root)

help_menu = Menu(Menuvar, tearoff=0)
help_menu.add_command(label="readme", command=readme_btn)
help_menu.add_command(label="IPアドレス一覧", command=all_ip_show)
help_menu.add_command(label="データを削除", command=delete_data)
help_menu.add_separator()


Menuvar.add_cascade(label="ヘルプ",menu=help_menu)


root.config(menu = Menuvar)

frame4 = tk.Frame(root, pady=10)
frame4.pack()

Save = ttk.Button(frame4)
Save["text"] = "セーブ"
Save["command"] = save_btn
Save.pack(side="left")

Login = ttk.Button(frame4)
Login["text"] = "ログイン"
Login["command"] = login
Login.pack(side="left")

if len(u_text) < 0 and len(p_text) < 0:
  Login.state(["disabled"])


Logout = ttk.Button(frame4)
Logout["text"] = "ログアウト"
Logout["command"] = logout
Logout.pack(side="left")


quit = ttk.Button(frame4, text="終了", command=root.destroy)
quit.pack(side="left")

root.mainloop()