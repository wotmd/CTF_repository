#!/usr/bin/env python3
from base64 import b64decode

def find(data):
	cnt = 0
	for j in range(128,1000):
		if(cnt>=100):
			return (j-cnt)
        elif data[cnt]==data[j]:
			cnt=cnt+1
		else:
			cnt=0
	return 0

if __name__ == "__main__":
	for i in range(2,128):
		f = open('tmp/'+str(i)+'.xor', 'rb')
		
		data = f.read()	
		a=find(data)
		if(a>0):
			print("good!!! filename is"+str(i)+".xor")
			print(a)
		
		f.close()