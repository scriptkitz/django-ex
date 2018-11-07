import os
import struct
import xml.etree.ElementTree as ET

from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse

from .ByteArray import ByteArray


module_dir = os.path.dirname(__file__)  # get current directory
# Create your views here.

def _cmd_10(ba):
    name = ba.readUTF()
    print("name:%s"%name)
    newba = ByteArray()
    newba.writeShort(10)
    if name == "配置信息":
        file_path = os.path.join(module_dir, 'weiqi_conf.xml')
        fs = open(file_path,'rb')
        data = fs.read()
        fs.close()
        newba.writeUTF(data)
        
    return newba.bytes

def _cmd_201(ba):
    device = ba.readInt()
    imei = ba.readUTF()
    lesson = ba.readByte()
    print("-----")
    print(type(lesson))
    print(lesson)
    file_path = os.path.join(module_dir, 'weiqi_conf.xml')
    tree = ET.parse(file_path)
    root = tree.getroot()
    root.find('info')[lesson-1].get('code')

def weiqicmd(request):
    body = request.body
    print(body)
    ba = ByteArray(_bytes)
    cmd = ba.readShort()
    data = ""
    if cmd == 10:
        data = _cmd_10(ba)
    elif cmd == 201:
        data = _cmd_201(ba)
    resp = HttpResponse()
    resp.write(data)
    return resp

