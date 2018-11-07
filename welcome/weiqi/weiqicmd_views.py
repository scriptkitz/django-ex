import os
import struct
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse

from . import database
from .models import PageView

import ByteArray

# Create your views here.

def _cmd10(_bytes):
    ba = ByteArray(_bytes)
    name = ba.readUTF()

    newba = ByteArray()
    newba.writeShort(10)
    resp = HttpResponse()
    if name == "配置信息":
        fs = open("weiqi_conf.xml",'rb')
        data = fs.read()
        fs.close()
        newba.writeShort(len(data))
        newba.writeUTF(data)
        
    resp.write(newba.bytes)
    return resp


def weiqicmd(request):
    body = request.body
    cmd = struct.unpack(">h",body[:4])[0]
    content = body[4:]
    if cmd == 10:
        resp = _cmd10(content)
    
    return resp

