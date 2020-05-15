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

