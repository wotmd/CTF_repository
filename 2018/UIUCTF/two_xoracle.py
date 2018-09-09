#!/usr/bin/env python3
from base64 import b64decode

def xor(data, data2):
    out = ''
    for n in range(len(data)):
        out += chr(ord(data[n]) ^ ord(data2[n]))
    return out

if __name__ == "__main__":
	for i in range(2,128):
		f = open('tmp/1.enc', 'rb')
		g = open('tmp/'+str(i)+'.enc', 'rb')
		
		data = f.read()	
		data2 = g.read()
		
		data = b64decode(data.encode("utf-8"))
		data2 = b64decode(data2.encode("utf-8"))
		
		xor_f = open('tmp/'+str(i)+'.xor', 'wb')
		xor_f.write(xor(data, data2))
		
		f.close()
		g.close()
		xor_f.close()