#!/usr/bin/env python
# coding: utf-8

import weibo

# 注册微博App后，可以获得app key和app secret，然后定义网站回调地址：
APP_KEY = '1571040794'
APP_SECRET = '1b74684411b6a1de7a27eb9e4b48c429'
# 客户端默认回调页
# 通常Mobile Native App没有服务器回调地址，您可以在应用控制台授权回调页处填写平台提供的默认回调页，该页面用户不可见，仅用于获取access token。
# OAuth2.0客户端默认回调页：https://api.weibo.com/oauth2/default.html
# http://open.weibo.com/wiki/%E6%8E%88%E6%9D%83%E6%9C%BA%E5%88%B6%E8%AF%B4%E6%98%8E#.E5.AE.A2.E6.88.B7.E7.AB.AF.E9.BB.98.E8.AE.A4.E5.9B.9E.E8.B0.83.E9.A1.B5
CALLBACK_URL = 'https://api.weibo.com/oauth2/default.html'

# 在网站放置“使用微博账号登录”的链接，当用户点击链接后，引导用户跳转至如下地址：
client = weibo.APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
url = client.get_authorize_url()
# TODO: redirect to url

# 用户授权后，将跳转至网站回调地址，并附加参数code=abcd1234：
# 获取URL参数code:
# code = your.web.framework.request.get('code')
code = '3d04372afee06631eca47ee11303d804'
client = weibo.APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
r = client.request_access_token(code)
access_token = r.access_token # 新浪返回的token，类似abc123xyz456
expires_in = r.expires_in # token过期的UNIX时间：http://zh.wikipedia.org/wiki/UNIX%E6%97%B6%E9%97%B4
print 'access_token expires_in: ', expires_in
# 获取access_token之后，可以保存起来，以后直接读，不用反复通过code来获取
# TODO: 在此可保存access token
client.set_access_token(access_token, expires_in)

# 然后，可调用任意API, 用户身份审核后：
print client.statuses.user_timeline.get()
print client.statuses.update.post(status=u'测试OAuth 2.0发微博')
