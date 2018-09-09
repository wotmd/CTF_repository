#!/usr/bin/env python3
from base64 import b64decode

f = open('Base64Decode.bin', 'rb')

data = f.read()	
f.close()

list = [0]*256


for n in range(len(data)):
	list[ord(data[n])]=list[ord(data[n])]+1
cnt=0;

replaceCHAR = [0]*500

for i,n in enumerate(list):
	if not n==0:
		print("index %d : %d", i, n)
		replaceCHAR[cnt]=i
		cnt=cnt+1
	
print("count : "+str(cnt))	
print("data_lne : "+str(len(data)))
charset = "!@#$%^&*()-=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

stri = ""

for n in range(len(data)):
	for i,c in enumerate(replaceCHAR):
		if(ord(data[n])==c):
			stri+=charset[i]

print(stri)

