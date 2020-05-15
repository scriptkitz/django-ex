#-*- coding=utf-8 -*-
import urllib
import base64
import time
import json
import sys

#无码

#PyVersion
g_isPy3 = sys.version_info.major == 3

if g_isPy3:
    import http.client as httplib
else:
    import httplib

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

class wumaStatic:
    def __init__(self):
        self._conn = httplib.HTTPConnection("hiwuma.xyz",80)
        self._headers = {
            "User-Agent":"okhttp/3.9.1",
            "Accept-Encoding":"gzip"
        }
        self._userId = ""
    def hellotxt(self):
        data = self._send("/wumavpn/wmapi/hello.txt")
        #self._save("hellotxt.json",data)
        jObj = json.loads(data)
        return jObj
    def testtxt(self):
        data = self._send("/wumavpn/wmapi/test.txt")
        #self._save("testtxt.json",data)
        jObj = json.loads(data)
        return jObj
    def testini(self):
        data = self._send("/wumavpn/wmapi/test.ini")
        self._save("testini.json",data)
        jObj = json.loads(data)
        return jObj
    def _send(self,uri):
        self._conn.request("GET",uri, headers=self._headers)
        resp = self._conn.getresponse()
        data = resp.read()
        return decryptResp(data)
    def _save(self,name,data):
        fs=open(str(time.time())+name,"wb")
        fs.write(data)
        fs.close()

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
