from struct import *

class ByteArray:
    def __init__(this, bytes=b""):
        this.bytes = bytes

    def writeByte(this, value):
        if type(value) == str:
            value = value.encode("utf-8")
        pass
        this.bytes += pack('!b', int(value))
        return this

    def writeUnsignedByte(this, value):
        if type(value) == str:
            value = value.encode("utf-8")
        pass
        this.bytes += pack('!B', int(value))
        return this

    def writeShort(this, value):
        if type(value) == str:
            value = value.encode("utf-8")
        pass
        this.bytes += pack('!h', int(value))
        return this

    def writeUnsignedShort(this, value):
        if type(value) == str:
            value = value.encode("utf-8")
        pass
        this.bytes += pack('!H', int(value))
        return this
    
    def writeInt(this, value):
        if type(value) == str:
            value = value.encode("utf-8")
        pass
        this.bytes += pack('!i', int(value))
        return this

    def writeUnsignedInt(this, value):
        if type(value) == str:
            value = value.encode("utf-8")
        pass
        this.bytes += pack('!I', int(value))
        return this

    def writeBoolean(this, value):
        if type(value) == str:
            value = value.encode("utf-8")
        pass
        this.bytes += pack('!?', int(value))
        return this

    def writeUTF(this, value):
        if type(value) == str:
            value = value.encode("utf-8")
        pass
        value = str(value)
        size = len(value)
        this.writeShort(size)
        this.write(value)
        return this

    def writeUTFBytes(this, value, size):
        if type(value) == str:
            value = value.encode("utf-8")
        pass
        for data in str(pack('!b', 0)) * int(size):
            if len(value) < int(size):
                value = value + pack('!b', 0)
        this.write(value)
        return this

    def writeBytes(this, value):
        this.bytes += value
        return this

    def write(this, value):
        this.bytes += value

    def readByte(this):
        value = unpack('!b', this.bytes[:1])[0]
        this.bytes = this.bytes[1:]
        return value

    def readUnsignedByte(this):
        value = unpack('!B', this.bytes[:1])[0]
        this.bytes = this.bytes[1:]
        return value

    def readShort(this):
        value = unpack('!h', this.bytes[:2])[0]
        this.bytes = this.bytes[2:]
        return value

    def readUnsignedShort(this):
        value = unpack('!H', this.bytes[:2])[0]
        this.bytes = this.bytes[2:]
        return value

    def readInt(this):
        value = unpack('!i', this.bytes[:4])[0]
        this.bytes = this.bytes[4:]
        return value
		
    def readUnsignedInt(this):
        value = unpack('!I', this.bytes[:4])[0]
        this.bytes = this.bytes[4:]
        return value

    def readUTF(this):
        size = unpack('!h', this.bytes[:2])[0]
        value = this.bytes[2:2 + size]
        this.bytes = this.bytes[size + 2:]
        return value.decode('utf-8')

    def readBoolean(this):
        value = unpack('!?', this.bytes[:1])[0]
        this.bytes = this.bytes[1:]
        return (True if value == 1 else False)

    def readUTFBytes(this, size):
        value = this.bytes[:int(size)]
        this.bytes = this.bytes[int(size):]
        return value

    def getLength(this):
        return len(this.bytes)

    def bytesAvailable(this):
        return len(this.bytes) > 0

    def toByteArray(this):
        return this.bytes
