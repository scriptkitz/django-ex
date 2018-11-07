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
    print("name:%s"%name)
    newba = ByteArray()
    newba.writeShort(10)
    if name == "配置信息":
        module_dir = os.path.dirname(__file__)  # get current directory
        file_path = os.path.join(module_dir, 'weiqi_conf.xml')
        fs = open(file_path,'rb')
        data = fs.read()
        fs.close()
        newba.writeShort(len(data))
        newba.writeUTF(data)
        
    return newba.bytes


def weiqicmd(request):
    body = request.body
    print(body)
    cmd = struct.unpack(">h",body[:2])[0]
    content = body[2:]
    data = ""
    if cmd == 10:
        data = _cmd10(content)
    resp = HttpResponse()
    resp.write(data)
    return resp

