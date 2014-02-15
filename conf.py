# -*- coding: utf-8 -*-
"""
Created on Feb 15, 2014

@author: honghe

APP配置信息
"""

# 注册微博App后，可以获得app key和app secret，然后定义网站回调地址：
APP_KEY = '1571040794'
APP_SECRET = '1b74684411b6a1de7a27eb9e4b48c429'
# 客户端默认回调页
# 通常Mobile Native App没有服务器回调地址，您可以在应用控制台授权回调页处填写平台提供的默认回调页，该页面用户不可见，仅用于获取access token。
# OAuth2.0客户端默认回调页：https://api.weibo.com/oauth2/default.html
# http://open.weibo.com/wiki/%E6%8E%88%E6%9D%83%E6%9C%BA%E5%88%B6%E8%AF%B4%E6%98%8E#.E5.AE.A2.E6.88.B7.E7.AB.AF.E9.BB.98.E8.AE.A4.E5.9B.9E.E8.B0.83.E9.A1.B5
CALLBACK_URL = 'https://api.weibo.com/oauth2/default.html'