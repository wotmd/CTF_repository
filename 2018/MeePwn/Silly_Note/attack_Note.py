import base64

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

enc = "J5GgRCbB1NfVAI68i7ZrFpThnQw9PgEwUTEWFV9XihZsteG8ROGFhK2c4zlgr+l0"

cipher = base64.b64decode(enc)

print("len : %d\n" % len(cipher))
print(cipher.encode("hex"))

