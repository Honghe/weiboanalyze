#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Feb 15, 2014

@author: honghe

API调用示例
"""

from initclient import initclient

def postweibo():
    client = initclient.get_client()
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
    client = initclient.get_client()
    if not client:
        print 'Get client Error!'
        return  
    r = client.statuses.public_timeline.get(count=20)
    for st in r.statuses:
        print st.text       

def fetch_user_timeline():
    client = initclient.get_client()
    if not client:
        print 'Get client Error!'
        return
    r = client.statuses.user_timeline.get()
    for st in r.statuses:
        print st.text

if __name__ == '__main__':
    fetch_public_timeline()