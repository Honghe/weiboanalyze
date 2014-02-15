#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Feb 15, 2014

@author: honghe

客户端初始化
"""
import weibo
import time
import os

# 从配置文件导入微博APP信息
config = {}
execfile(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../conf.py"), config) 
# python 3: exec(open("example.conf").read(), config)
APP_KEY = config['APP_KEY']
APP_SECRET = config['APP_SECRET']
CALLBACK_URL = config['CALLBACK_URL']

class aAPIClient(weibo.APIClient):
    """
    myAPIClient类继承自weibo包中的APIClient类，对其进行了扩展。SDK中的APIClient类没有根据已授权的access_token获取授权详细信息的接口。
    另外，SDK中的APIClient不能保存当前授权用户的uid，该继承类实现了这两个功能，使得用起来更加方便。 
    """
    def __init__(self, app_key, app_secret, redirect_uri=None, response_type='code', domain='api.weibo.com', version='2'):
        super(aAPIClient, self).__init__(app_key, app_secret, redirect_uri, response_type=response_type, domain=domain, version=version)
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
    filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
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

# TODO duplicated access_token dump
def dump_tokens(access_token, filename=TOKEN_FILE):
    filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
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

def get_client(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL):
    # 在网站放置“使用微博账号登录”的链接，当用户点击链接后，引导用户跳转至如下地址：
    client = aAPIClient(app_key, app_secret, redirect_uri)
    access_token_list = load_tokens()
    # 若有已存储的access_token，使用它
    if access_token_list:
        access_token = access_token_list[-1]
        r = client.request_access_token_info(access_token)
        expires_in = r.expires_in
        print '=> The access_token expires_in : %f' % expires_in
        # 授权access_token过期
        if r.expires_in <= 0:
            return None
        client.set_uid(r.uid)
    # 若没有已存储的access_token，调用API获取
    else:
        auth_url = client.get_authorize_url()
        # TODO: redirect to url
        print '=> auth_url : %s' % auth_url  
        print '=> Note! The access_token is not available, you should be authorized again. Please open the url above in your browser, then you will get a returned url with the code field. Input the code in the follow step.'
        # 用户授权后，将跳转至网站回调地址，并附加参数code=abcd1234：
        # 获取URL参数code:
        # code = your.web.framework.request.get('code')
        code = raw_input('=> input the retured code:')
        r = client.request_access_token(code)
        access_token = r.access_token   # 新浪返回的token，类似abc123xyz456
        expires_in = r.expires_in   # token过期的UNIX时间：http://zh.wikipedia.org/wiki/UNIX%E6%97%B6%E9%97%B4
        print '=> the new access_token is : %s' % access_token 
        print 'access_token expires_in: ', expires_in
        dump_tokens(access_token) 

    client.set_access_token(access_token, expires_in)  
    client.set_uid(r.uid)  
    # 然后，可调用任意API, 用户身份审核后：
    return client  
