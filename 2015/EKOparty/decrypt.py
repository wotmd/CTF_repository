import struct
import sys
import base64

crypt="CjBPewYGc2gdD3RpMRNfdDcQX3UGGmhpBxZhYhFlfQA="

print base64.b64decode(crypt)
plain=base64.b64decode(crypt)

blocks2 = struct.unpack("I" * (len(plain) / 4), plain)

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