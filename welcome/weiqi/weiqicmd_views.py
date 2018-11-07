import os
import struct
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse

from .ByteArray import ByteArray

# Create your views here.

def _cmd10(_bytes):
    ba = ByteArray(_bytes)
    name = ba.readUTF()

    newba = ByteArray()
    newba.writeShort(10)
    if name == "配置信息":
        fs = open("weiqi_conf.xml",'rb')
        data = fs.read()
        fs.close()
        newba.writeShort(len(data))
        newba.writeUTF(data)
        
    return newba.bytes


def weiqicmd(request):
    body = request.body
    cmd = struct.unpack(">h",body[:2])[0]
    content = body[2:]
    data = ""
    if cmd == 10:
        data = _cmd10(content)
    resp = HttpResponse()
    resp.write(data)
    return resp

