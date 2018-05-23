#!/usr/bin/python
# -*- coding:utf-8-*-
import http.client
import time
import os
def get_webservertime(host):
    conn=http.client.HTTPConnection(host)
    conn.request("GET", "/")
    r=conn.getresponse()
    #r.getheaders() #获取所有的http头
    ts=  r.getheader('date') #获取http头date部分
    #将GMT时间转换成北京时间
    ltime= time.strptime(ts[5:25], "%d %b %Y %H:%M:%S")
    '''
    print(ltime)
    ttime=time.localtime(time.mktime(ltime)+8*60*60)
    print(ttime)
    dat="date %u-%02u-%02u"%(ttime.tm_year,ttime.tm_mon,ttime.tm_mday)
    tm="time %02u:%02u:%02u"%(ttime.tm_hour,ttime.tm_min,ttime.tm_sec)
    print (dat,tm)
    os.system(dat)
    os.system(tm)
    '''
    return ltime

def validateT():
    now = get_webservertime('www.baidu.com')
    maxTs = '20180221000001'
    maxT = time.strptime(maxTs,'%Y%m%d%H%M%S')
    if now > maxT:
        return False
    else:
        return True
'''        
if validateT():
    print ("continue")
else:
    print("expired!")
'''