#!/usr/bin/env python
# coding: utf-8

import weibo
import time
import os

# # 注册微博App后，可以获得app key和app secret，然后定义网站回调地址：
# APP_KEY = '1571040794'
# APP_SECRET = '1b74684411b6a1de7a27eb9e4b48c429'
# # 客户端默认回调页
# # 通常Mobile Native App没有服务器回调地址，您可以在应用控制台授权回调页处填写平台提供的默认回调页，该页面用户不可见，仅用于获取access token。
# # OAuth2.0客户端默认回调页：https://api.weibo.com/oauth2/default.html
# # http://open.weibo.com/wiki/%E6%8E%88%E6%9D%83%E6%9C%BA%E5%88%B6%E8%AF%B4%E6%98%8E#.E5.AE.A2.E6.88.B7.E7.AB.AF.E9.BB.98.E8.AE.A4.E5.9B.9E.E8.B0.83.E9.A1.B5
# CALLBACK_URL = 'https://api.weibo.com/oauth2/default.html'

class aAPIClient(weibo.APIClient):
    """
    myAPIClient类继承自weibo包中的APIClient类，对其进行了扩展。SDK中的APIClient类没有根据已授权的access_token获取授权详细信息的接口。
    另外，SDK中的APIClient不能保存当前授权用户的uid，该继承类实现了这两个功能，使得用起来更加方便。 
    """
    def __init__(self, app_key, app_secret, redirect_uri=None, response_type='code', domain='api.weibo.com', version='2'):
        super(aAPIClient, self).__init__(app_key, app_secret, redirect_uri, response_type='code', domain='api.weibo.com', version='2')
        # 保存当前授权用户的uid
        self.uid = ''
        
    def request_access_token_info(self, access_token):
        """
        该接口传入参数access_token为已经授权的access_token，函数将返回该access_token的详细信息，返回Json对象，与APIClient类的request_access_token类似。
        """
        r = weibo._http_post('%s%s' % (self.auth_url, 'get_token_info'), access_token = access_token)
        # TODO 此处时间rtime，expires比较用处是何？
        current = int(time.time())
        expires = r.expire_in + current
        remind_in = r.get('remind_in', None)
        if remind_in:
            rtime = int(remind_in) + current
            if rtime < expires:
                expires = rtime
        return weibo.JsonDict(expires=expires, expires_in=expires, uid=r.get('uid', None))

    def set_uid(self, uid):
        self.uid = uid

TOKEN_FILE = 'access_token.txt'
def load_tokens(filename=TOKEN_FILE):
    access_token_list = []
    filepath = os.path.join(os.path.dirname(__file__), filename)
    # TODO better process logic
    if not os.path.exists(filepath):
        print "file %s not exist." % filepath
        return None
    try:
        f = open(filepath)
        # 防止list添加空的''
        access_token = f.readline().strip()
        if access_token:
            access_token_list.append(access_token)
            print '=> Get the access_token from file %s: %s' % (TOKEN_FILE, access_token_list[0]) 
    except IOError, e:
        raise e
    finally:
        f.close()
    return access_token_list

def dump_tokens(access_token, filename=TOKEN_FILE):
    filepath = os.path.join(os.path.dirname(__file__), filename)
    if not os.path.exists(filepath):
        print "file %s not exist." % filepath
        return None
    try:
        f = open(filepath, 'a+')
        f.write(access_token)
        f.write('\n')
    except IOError, e:
        raise e
    finally:
        f.close()

def get_client(app_key, app_secret, redirect_uri):
    client = aAPIClient(app_key, app_secret, redirect_uri)
    access_token_list = load_tokens()
    if access_token_list:
        access_token = access_token_list[-1]
        r = client.request_access_token_info(access_token)
        expires_in = r.expires_in
        print '=> The access_token expires_in : %f' % expires_in
        # 授权access_token过期
        if r.expires_in <= 0:
            return None
        client.set_uid(r.uid)
    else:
        auth_url = client.get_authorize_url()
        print '=> auth_url : %s' % auth_url  
        print '=> Note! The access_token is not available, you should be authorized again. Please open the url above in your browser, then you will get a returned url with the code field. Input the code in the follow step.'
        code = raw_input('=> input the retured code:')
        r = client.request_access_token(code)
        access_token = r.access_token
        expires_in = r.expires_in
        print '=> the new access_token is : %s' % access_token 
        dump_tokens(access_token) 

    client.set_access_token(access_token, expires_in)  
    client.set_uid(r.uid)  
    return client  
    
##################################################################
# # 在网站放置“使用微博账号登录”的链接，当用户点击链接后，引导用户跳转至如下地址：
# client = weibo.APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
# url = client.get_authorize_url()
# # TODO: redirect to url

# # 用户授权后，将跳转至网站回调地址，并附加参数code=abcd1234：
# # 获取URL参数code:
# # code = your.web.framework.request.get('code')
# code = '3d04372afee06631eca47ee11303d804'
# client = weibo.APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
# r = client.request_access_token(code)
# access_token = r.access_token # 新浪返回的token，类似abc123xyz456
# expires_in = r.expires_in # token过期的UNIX时间：http://zh.wikipedia.org/wiki/UNIX%E6%97%B6%E9%97%B4
# print 'access_token expires_in: ', expires_in
# # 获取access_token之后，可以保存起来，以后直接读，不用反复通过code来获取
# # TODO: 在此可保存access token
# client.set_access_token(access_token, expires_in)

# # 然后，可调用任意API, 用户身份审核后：
# print client.statuses.user_timeline.get()
# print client.statuses.update.post(status=u'测试OAuth 2.0发微博')
