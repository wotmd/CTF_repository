import socket

BLOCK_SIZE = 16

def check_pad(cipher):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect(('18.223.150.0', 3141))
	sock.send(cipher)
	result = ""
	for i in range(0x20,0x40):
		result += sock.recv(1)
	sock.close()
	return result
	
def unpadding_pkcs7(block):
	len_b = len(block)
	n_padd = ord(block[-1])
	if(n_padd==0):
		raise ValueError('bad padding')
	for c in range(0, n_padd):
		if(n_padd != ord(block[len_b-1-c])):
			raise ValueError('bad padding')
			
	unpad_block = block[:-n_padd]
	return unpad_block

def get_nextBlock_decrypt(cipher, iv):
	knownP = ""
	for padding_len in range(1,BLOCK_SIZE+1):
		candiP = ""
		result = ""
		for startIdx in range(0x0, 0x81, 0x20):
			sendFeed = ""
			for i in range(startIdx,startIdx+0x20):
				makeIV = "\x00"*(BLOCK_SIZE-padding_len) + chr(i ^ ord(iv[-padding_len]) ^ padding_len)
				for j in range(0,len(knownP)):
					makeIV += chr(ord(iv[len(makeIV)]) ^ ord(knownP[j]) ^ padding_len)
				sendFeed += str(len(makeIV+cipher))+makeIV+cipher
			result += check_pad(sendFeed)
		print(result)
		candiP = result.find("1")
		candiP=chr(candiP)
		knownP = candiP + knownP
	return knownP
	
def OraclePaddingAttack(cipher):
	KnownP = ""
	ciphers = []
	for i in range(0, len(cipher), BLOCK_SIZE):
		ciphers.append(cipher[i:i+BLOCK_SIZE])
	for i, c in enumerate(ciphers[1:]):
		preIV = ciphers[i]
		KnownP += get_nextBlock_decrypt(c, preIV)
		print(KnownP)
	return KnownP


cipher = open("Encrypted.txt","r").read()
print("len : %d " % len(cipher))
plain = OraclePaddingAttack(cipher)
print(plain)

