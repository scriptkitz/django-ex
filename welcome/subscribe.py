#-*- coding=utf-8 -*-
import re
import ssl
from django.shortcuts import render
from django.http import StreamingHttpResponse, HttpResponse

import uuid
import os
import sys
import os.path
import urllib
import base64
import hashlib
import time
import json
import urllib.parse

from Crypto.Cipher import AES

#PyVersion
g_isPy3 = sys.version_info.major == 3

AES_BS = AES.block_size
AES_pad =lambda s: s +(AES_BS - len(s)% AES_BS)* chr(AES_BS - len(s)% AES_BS)
if g_isPy3:
    AES_unpad =lambda s : s[0:-s[-1]]
else:
    AES_unpad =lambda s : s[0:-ord(s[-1])]


if g_isPy3:
    import http.client as httplib
else:
    import httplib

g_BuyVIP = True
DEVICE_ID = "202abd5713621f79"

SS_DEFAULT_ENCRYPT = "rc4-md5"
SS_DEFAULT_PASSWORD= "QAZXSW12345PLM987"

TOKEN_FILE_NAME = "lvye_%s_token.txt"%DEVICE_ID

context = ssl._create_unverified_context()

class lvYe:
    def __init__(self):
        self._conn = httplib.HTTPConnection("nacl.cc",80)#"95.163.196.113",80) #fastjet.info
        self._aesKey = self._getAESkey()
        self._headers = {
            "User-Agent":"okhttp/3.9.1",
            "deviceID":DEVICE_ID,
            "Accept-Encoding":"gzip",
            "time":"",
            "token": ""
        }
        self._userId = ""
        self._obj = None

    def getpng(self):
        data = self._send("/auth/v1/code")
        b64img = json.loads(data)['data']
        img = base64.decodebytes(b64img.encode('gbk')) if g_isPy3 else base64.decodestring(b64img)
        fs = open('welcome/static/code.png','wb')
        fs.write(img)
        fs.close()

    def auth(self,code):
        data = self._send("/auth/v1/token?authCode=%s"%code)
        obj = json.loads(data)
        if obj['code']==200:
            token = obj['data']
            self._headers['token'] = token
            self._writeToken(token)
            return True
        else:
            #print(obj['msg'])
            return False
    def checklogin(self):
        if not self._checkToken():
            return False
        data = self._send("/api/v9/member/login?deviceId=%s"%DEVICE_ID)
        rObj = json.loads(data)
        if(rObj['code']==500):
            return False
        obj = rObj['data']
        self._obj = obj
        self._userId = obj['memberInfo']['userId']
        return True
    def adClick(self):
        """点击广告赚绿叶币"""
        data = self._send("/api/v9/member/adClick?userId=%s"%self._userId)
        obj = json.loads(data)
        print(obj)
    def checkIn(self):
        """签到"""
        data = self._send("/api/v9/member/checkIn?userId=%s"%self._userId)
        obj = json.loads(data)
        print(obj)
    def buyLeafCoinProduct(self):
        """140绿叶币换1日黄金会员"""
        data = self._send("/api/v9/shop/buyLeafCoinProduct?userId=%s&productId=3"%self._userId)
        obj = json.loads(data)
        print(obj)
    def _send(self,uri):
        self._headers["time"] = self._getTimeStr()
        self._conn.request("GET",uri, headers=self._headers)
        resp = self._conn.getresponse()
        data = resp.read()
        return self._decryptResp(data)

    def _getAESkey(self):
        xstr = self._getTimeStr() + "@@" + DEVICE_ID + "@@" + "1qazxsw2"
        md5 = hashlib.md5()
        if g_isPy3: xstr = xstr.encode('gbk')
        md5.update(xstr)
        digest = md5.hexdigest()
        aesKey = digest[8:24]
        bs = aesKey.encode('gbk') if g_isPy3 else aesKey
        return bs

    def _getTimeStr(self):
        return time.strftime("%Y-%m-%d",time.gmtime())

    def _decryptResp(self,data):
        data = base64.decodebytes(data) if g_isPy3 else base64.decodestring(data)
        aesObj = AES.new(self._aesKey, mode=AES.MODE_CBC, IV=self._aesKey)
        return AES_unpad(aesObj.decrypt(data))
    
    def _writeToken(self,token):
        fs = open(TOKEN_FILE_NAME,'wb')
        if g_isPy3: token = token.encode('gbk')
        fs.write(token)
        fs.close()
    def _readToken(self):
        token = ""
        if os.path.isfile(TOKEN_FILE_NAME):
            fs = open(TOKEN_FILE_NAME,"r")
            token = fs.read()
            fs.close()
        return token
    def _checkToken(self):
        token = self._readToken()
        if token:
            self._headers['token'] = token
            return True
        return False

def decryptResp(data):
    while True:
        pos = data.find(b"Wwosxbg")
        if pos != -1:
            data = data[:pos-6] + data[pos+18:]
        else:
            pos = data.find(b"WeqBoew")
            if pos != -1:
                data = data[:pos] + data[pos+24:]
            else:
                break
    data = base64.decodestring(data)
    return data

class wumaPhp:
    def __init__(self):
        self._conn = httplib.HTTPConnection("176.122.140.202",7777)
        self._headers = {
            "User-Agent":"okhttp/3.9.1",
            "Accept-Encoding":"gzip",
            "Content-Type": "application/x-www-form-urlencoded"
        }
    def hi(self):
        body = {
            "is_gp": "0",
            "time": str(time.time()).replace(".",""),
            "token": "HnxeJnHW3k4AyqX9lBUcG74sad1zKAyKepb",
            "ver_code": 323,
            "chn_name": "git_v2",
            "lang": "zh-CN",
            "sys_ver": 22,
            "uid": "HnxeJ",
            "dev_id": "2018062509580352265773",
            "pkg": "com.muma.pn",
            "brd_mod": "Nokia N8010"
        }
        if g_isPy3:
            sbody = urllib.parse.quote(base64.encodestring(json.dumps(body).encode('gbk')))
        else:
            sbody = urllib.quote(base64.encodestring(json.dumps(body)))
        sbody = sbody[:10] + "9328WRewosxbg39823B98weB" + sbody[10:]
        sbody = sbody[:70] + "323284Wwosxbg9873298ewIE" + sbody[70:]
        sbody = "data=" + sbody
        data = self._send("/index.php/wmapp/hi",sbody)
        #self._save("hellotxt",data)
        jObj = json.loads(data)
        return jObj

    def _send(self,uri,body=None):
        self._conn.request("POST",uri,body, headers=self._headers)
        resp = self._conn.getresponse()
        data = resp.read()
        return decryptResp(data)

    def _save(self,name,data):
        fs=open(name+"_%d.json"%time.time(), "wb")
        fs.write(data)
        fs.close()


def subscribe(request):
    o = lvYe()
    if 'code' in request.GET:
        if not o.auth(request.GET.get('code')):
            o.getpng()
            return render(request, 'subscribe/auth.html', {'imgsrc': 'static/code.png'})

    if not o.checklogin():
        o.getpng()
        return render(request, 'subscribe/auth.html', {'imgsrc': 'static/code.png'})
    else:
        u = o._obj
        #广告
        i = u['everyDayInfo']['clickAdCount']
        while i>0:
            o.adClick()
            i-=1
        #签名
        if not u['everyDayInfo']["punch"]:
            o.checkIn()
        #购买VIP
        if u['memberInfo']["vipType"]:
            startvip = time.strptime(u['memberInfo']['vipStartTime'].split(".")[0], "%Y-%m-%dT%H:%M:%S")
            endvip = time.strptime(u['memberInfo']['vipEndTime'].split(".")[0], "%Y-%m-%dT%H:%M:%S")
            newtime = time.localtime()
            if newtime >= endvip:
                o.buyLeafCoinProduct()
                o.checklogin()
        else:
            o.buyLeafCoinProduct()
            o.checklogin()
        u = o._obj
        servers = u['freeServerInfos']
        if u['memberInfo']['vipType'] > 0:
            servers.extend(u['vipServerInfos'])
        contentstr = []
        for sv in servers:
            host = sv['host']
            if host == "0.0.0.0":continue
            strvip = "vip_" if sv['type'] == 0 else ""
            encrypt = sv['encrypt'] if sv['encrypt'] else SS_DEFAULT_ENCRYPT
            password = sv['password'] if sv['password'] else SS_DEFAULT_PASSWORD
            c = encrypt+":"+password+"@"+host+":"+str(sv['minPort'])
            conf = "ss://" + base64.standard_b64encode(c.encode('gbk')).decode('gbk') + "#" + urllib.parse.quote(strvip+sv['countryName'])
            contentstr.append(conf)
            
        return HttpResponse(base64.standard_b64encode('\n'.join(contentstr).encode('gbk')).decode('gbk'))
    #return StreamingHttpResponse(go())



def subscribe2(request):
    o=wumaPhp()
    jo = o.hi()

    contentstr = []
    for gp in jo['d']['gp']:
        gplist = gp['list']
        for sv in gplist:
            sid = "wuma_%s_"%gp['name'][-2:]
            c = sv['md']+":"+sv['pd']+"@"+sv['ip']+":"+str(int(sv['pt']))
            conf = "ss://" + base64.standard_b64encode(c.encode('gbk')).decode('gbk') + "#" + urllib.parse.quote(sid+sv['lb'])
            contentstr.append(conf)
    return HttpResponse(base64.standard_b64encode('\n'.join(contentstr).encode('gbk')).decode('gbk'))