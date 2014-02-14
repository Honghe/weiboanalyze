#!/usr/bin/env python
# coding: utf-8

from initclient import initclient

# 注册微博App后，可以获得app key和app secret，然后定义网站回调地址：
APP_KEY = '1571040794'
APP_SECRET = '1b74684411b6a1de7a27eb9e4b48c429'
# 客户端默认回调页
# 通常Mobile Native App没有服务器回调地址，您可以在应用控制台授权回调页处填写平台提供的默认回调页，该页面用户不可见，仅用于获取access token。
# OAuth2.0客户端默认回调页：https://api.weibo.com/oauth2/default.html
# http://open.weibo.com/wiki/%E6%8E%88%E6%9D%83%E6%9C%BA%E5%88%B6%E8%AF%B4%E6%98%8E#.E5.AE.A2.E6.88.B7.E7.AB.AF.E9.BB.98.E8.AE.A4.E5.9B.9E.E8.B0.83.E9.A1.B5
CALLBACK_URL = 'https://api.weibo.com/oauth2/default.html'

def postweibo():
    client = initclient.get_client(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
    if not client:
        print 'Get client Error!'
        return

    # 发微博
    while True:
        print 'Do you want to send a new weibo?(y/n):',
        choice = raw_input()
        if choice in ['y','Y']:
            content = raw_input('Input new weibo content:')
            if content:
                client.statuses.update.post(status = content)
                print 'Send succesfully!'
                break;
            else:
                print 'Error! Empty content!'
        if choice in ['n', 'N']:
            break

def fetch_public_timeline():
    client = initclient.get_client(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
    if not client:
        print 'Get client Error!'
        return  
    r = client.statuses.public_timeline.get(count=20)
    for st in r.statuses:
        print st.text   

def fetch_user_timeline():
    client = initclient.get_client(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
    if not client:
        print 'Get client Error!'
        return
    r = client.statuses.user_timeline.get()
    for st in r.statuses:
        print st.text

if __name__ == '__main__':
    fetch_public_timeline()