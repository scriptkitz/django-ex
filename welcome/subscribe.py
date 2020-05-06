#-*- coding=utf-8 -*-
import re
import ssl
from django.shortcuts import render
from django.http import StreamingHttpResponse, HttpResponse

import os
import sys
import os.path
import urllib
import base64
import hashlib
import time
import json

try:
    from Crypto.Cipher import AES
    AES_BS = AES.block_size
    AES_pad =lambda s: s +(AES_BS - len(s)% AES_BS)* chr(AES_BS - len(s)% AES_BS)
    if g_isPy3:
        AES_unpad =lambda s : s[0:-s[-1]]
    else:
        AES_unpad =lambda s : s[0:-ord(s[-1])]
    needpycryptodome = False
except:
    needpycryptodome = True

#PyVersion
g_isPy3 = sys.version_info.major == 3

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
        self._conn = httplib.HTTPConnection("nacl.cc",80)#"95.163.196.113",80)
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
        fs = open('code.png','wb')
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
        data = self._send("/api/v6/member/login?deviceId=%s"%DEVICE_ID)
        rObj = json.loads(data)
        if(rObj['code']==500):
            return False
        obj = rObj['data']
        self._obj = obj
        self._userId = obj['memberInfo']['userId']
        return True
    def adClick(self):
        """点击广告赚绿叶币"""
        data = self._send("/api/v6/member/adClick?userId=%s"%self._userId)
        obj = json.loads(data)
        print(obj)
    def checkIn(self):
        """签到"""
        data = self._send("/api/v7/member/checkIn?userId=%s"%self._userId)
        obj = json.loads(data)
        print(obj)
    def buyLeafCoinProduct(self):
        """140绿叶币换1日黄金会员"""
        data = self._send("/api/v6/shop/buyLeafCoinProduct?userId=%s&productId=3"%self._userId)
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
        bs = aesKey.encode('ansi') if g_isPy3 else aesKey
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
        else:
            return self.auth()
        return False

def subscribe(request):
    if needpycryptodome:
        return HttpResponse("need oc rsh, install pycryptodome!")


    o = lvYe()
    if 'code' in request.GET:
        if not o.auth(request.GET.get('code')):
            o.getpng()
            return render(request, 'subscribe/auth.html', {'imgsrc': 'code.png'})

    if not o.checklogin():
        o.getpng()
        return render(request, 'subscribe/auth.html', {'imgsrc': 'code.png'})
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
            encrypt = sv['encrypt'] if sv['encrypt'] else SS_DEFAULT_ENCRYPT
            password = sv['password'] if sv['password'] else SS_DEFAULT_PASSWORD
            strvip = "vip_" if sv['type'] == 0 else ""
            countryName = sv['countryName'].encode('gbk')
            b64mark = base64.encodebytes(countryName) if g_isPy3 else base64.encodestring(countryName)
            host = sv['host']
            if host == "0.0.0.0":continue
            contentstr.append( ''.join((
                host,
                sv['minPort'],
                password,
                encrypt,
                'lvye_'+ strvip + sv['countryName'] + '%d'%i))
            )
        return HttpResponse(''.join(contentstr))
    #return StreamingHttpResponse(go())



