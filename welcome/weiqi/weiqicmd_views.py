import os
import struct
import xml.etree.ElementTree as ET

from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse

from .ByteArray import ByteArray


module_dir = os.path.dirname(__file__)  # get current directory
DEVICE_ID = 100
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
    elif name == "self":
        file_path = os.path.join(module_dir, '2.txt')
        fs = open(file_path,'rb')
        data = fs.read()
        fs.close()
        newba.writeUTF(data)
        
    return newba.bytes
def _cmd_100(ba):
    device = ba.readInt()
    imei = ba.readUTF()
    channel = ba.readUTF()
    version = ba.readUTF()
    print("---100---(%d)(%s)(%s)(%s)"%(device, imei, channel, version))
    
    newba = ByteArray()
    newba.writeShort(100)

    newba.writeInt(DEVICE_ID)
    newba.writeInt(111)
    newba.writeUTF("")

    return newba.bytes


def _cmd_201(ba):
    device = ba.readInt()
    imei = ba.readUTF()
    lesson = ba.readByte()
    print("---201---(%d)"%lesson)
    
    #file_path = os.path.join(module_dir, 'weiqi_conf.xml')
    #tree = ET.parse(file_path)
    #root = tree.getroot()
    #code = root.find('info')[lesson-1].get('code')

    newba = ByteArray()
    newba.writeShort(201)

    newba.writeByte(1)
    newba.writeInt(DEVICE_ID)
    
    t1 = 1
    t2 = 1
    t3 = DEVICE_ID*t2 - t1*lesson
    
    v1 = t1 << 3
    v2 = t2 << 2
    v3 = t3 << 1
    code = "%d,%d,%d"%(v1,v2,v3)
    
    newba.writeUTF(code)

    return newba.bytes

def weiqicmd(request):
    body = request.body
    print(body)
    ba = ByteArray(body)
    cmd = ba.readShort()
    data = ""
    if cmd == 10:
        data = _cmd_10(ba)
    elif cmd == 201:
        data = _cmd_201(ba)
    elif cmd == 100:
        data = _cmd_100(ba)
    resp = HttpResponse()
    resp.write(data)
    return resp

