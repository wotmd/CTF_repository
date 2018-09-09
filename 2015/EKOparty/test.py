import struct
import sys
import base64

if len(sys.argv) != 2:
    print "Usage: %s data" % sys.argv[0]
    exit(0)

data = sys.argv[1]
padding = 4 - len(data) % 4
if padding != 0:
    data = data + "\x42" * padding
	
print data

result = []
blocks = struct.unpack("I" * (len(data) / 4), data)

#unpack I*(4roTlr RMfgdjtj) abcdBBBB>> (int BBBB, int dcba)
#16.. (0x42424242,0x64636261)

print blocks
for block in blocks:
    result += [block ^ block >> 16]

print bin(0b1111^0b1111>>2)
print result
	
output = ''
for block in result:
    output += struct.pack("I", block)

print output
print len(output)

print base64.b64encode(output)

crypt=base64.b64encode(output)

print base64.b64decode(crypt)
plain=base64.b64decode(crypt)

blocks2 = struct.unpack("I" * (len(output) / 4), plain)

print "test : ",
print blocks2

result2 = []
for block in blocks2:
    result2 += [block ^ block >> 16]
	
print result2

output2 = ''
for block in result2:
    output2 += struct.pack("I", block)
	
print output2