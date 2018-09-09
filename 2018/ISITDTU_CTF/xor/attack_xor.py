#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Letter Distribution - Exterior Memory  http://www.macfreek.nl/memory/Letter_Distribution
freq = {
' ' : 18.28846265,
'E' : 10.26665037,
'T' : 7.51699827,
'A' : 6.53216702,
'O' : 6.15957725,
'N' : 5.71201113,
'I' : 5.66844326,
'S' : 5.31700534,
'R' : 4.98790855,
'H' : 4.97856396,
'L' : 3.31754796,
'D' : 3.28292310,
'U' : 2.27579536,
'C' : 2.23367596,
'M' : 2.02656783,
'F' : 1.98306716,
'W' : 1.70389377,
'G' : 1.62490441,
'P' : 1.50432428,
'Y' : 1.42766662,
'B' : 1.25888074,
'V' : 0.79611644,
'K' : 0.56096272,
'X' : 0.14092016,
'J' : 0.09752181,
'Q' : 0.08367550,
'Z' : 0.05128469,

'1' : 5.66844326, #I
'4' : 6.53216702, #A
'5' : 5.31700534, #S
'3' : 10.26665037,#E
'0' : 6.15957725, #O
'_' : 18.28846265,#_

'{' : 3.0,
'}' : 3.0,
}
def alphabet_score(stringA):
	score = 0.0
	for c in stringA:
		c=c.upper()
		if c in freq:
			score+=freq[c]
	return score

def XOR_singleByte(str1, sbyte):
	result = ""
	for i in range(0,len(str1),2):
		h1 = int(str1[i:i+2],16)
		h2 = sbyte
		result+= '{:02x}'.format(h1^h2)
	return result

def XOR_with_Key(str1, Key):
	result = ""
	keylen=len(Key)
	for i in range(0,len(str1),2):
		h1 = int(str1[i:i+2],16)
		h2 = ord(Key[(i/2)%keylen])
		result+= '{:02x}'.format(h1^h2)
	return result

def Hamming_distance(str1, str2):
	d = 0
	for i in range(0, len(str1)):
		hd = ord(str1[i]) ^ ord(str2[i])
		while hd > 0:
			d += (hd & 0x1)
			hd = hd>>1
	return d
	
enc_flag = "1d14273b1c27274b1f10273b05380c295f5f0b03015e301b1b5a293d063c62333e383a20213439162e0037243a72731c22311c2d261727172d5c050b131c433113706b6047556b6b6b6b5f72045c371727173c2b1602503c3c0d3702241f6a78247b253d7a393f143e3224321b1d14090c03185e437a7a607b52566c6c5b6c034047"
cipher = enc_flag.decode("hex")

KEY_LEN = 10
BLOCK_LEN = len(cipher)/KEY_LEN

blocks = [""]*BLOCK_LEN
for i in range(len(cipher)):
	blocks[i%BLOCK_LEN]+=cipher[i]

ciphers = ["",""]

for i, b in enumerate(blocks):
	if i % 2 != 0:
		ciphers[0] += b
	else:
		ciphers[1] = b + ciphers[1]

		
distance = 0.0
n = (len(ciphers[0])/(KEY_LEN))-1
for bsize in range(0,len(ciphers[0])-2*KEY_LEN,KEY_LEN):
	b1=ciphers[0][bsize:bsize+KEY_LEN]
	b2=ciphers[0][bsize+KEY_LEN:bsize+KEY_LEN*2]
	distance += Hamming_distance(b1, b2)

d=(distance/(n*KEY_LEN))

print("hamming_distance1 : %f" % d)
		
distance = 0.0
n = (len(ciphers[1])/(KEY_LEN))-1
for bsize in range(0,len(ciphers[1])-2*KEY_LEN,KEY_LEN):
	b1=ciphers[1][bsize:bsize+KEY_LEN]
	b2=ciphers[1][bsize+KEY_LEN:bsize+KEY_LEN*2]
	distance += Hamming_distance(b1, b2)

d=(distance/(n*KEY_LEN))

print("hamming_distance2 : %f" % d)	
	
keyString = ""
cipher = ciphers[0]+ciphers[1]

for i in range(0, KEY_LEN):
	Max_score = 0.0
	score = 0.0
	key = 0
	for sbyte in range(0,255):
		nCaesar = ""
		for j in range(i, len(cipher), KEY_LEN):
			nCaesar += cipher[j]
		nCaesar = nCaesar.encode("hex")
		nResult = XOR_singleByte(nCaesar, sbyte)
		nomal_string = nResult.decode("hex")
		
		score = alphabet_score(nomal_string)
	
		if score > Max_score:
			Max_score = score
			key = sbyte
	keyString += chr(key)

print("KeyString :"),
print(keyString)

print("\nPlaintext : ")
plain1 = XOR_with_Key(ciphers[0].encode("hex") ,keyString).decode("hex")
plain2 = XOR_with_Key(ciphers[1].encode("hex") ,keyString).decode("hex")
plain2 = plain2[::-1]

plain = ""
for i in range(BLOCK_LEN/2+1):
	plain += plain2[i*KEY_LEN:(i+1)*KEY_LEN] + plain1[i*KEY_LEN:(i+1)*KEY_LEN]

print(plain)