import socket

BLOCK_SIZE = 16

def check_pad(cipher):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect(('18.223.150.0', 3141))
	sock.send(str(len(cipher)))
	sock.send(cipher)
	result = sock.recv(1)
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
		for i in range(256):
			makeIV = "\x00"*(BLOCK_SIZE-padding_len) + chr(i ^ ord(iv[-padding_len]) ^ padding_len)
			for j in range(0,len(knownP)):
				makeIV += chr(ord(iv[len(makeIV)]) ^ ord(knownP[j]) ^ padding_len)
			if check_pad(makeIV + cipher) == "1":
				candiP += chr(i)
		if len(candiP) != 1:
			print(candiP)
			print("No!!")
			knownP = candiP[0] + knownP
		else:
			knownP = candiP + knownP
		print(candiP)
	return knownP
	
def OraclePaddingAttack(cipher):
	KnownP = ""
	ciphers = []
	for i in range(0, len(cipher), BLOCK_SIZE):
		ciphers.append(cipher[i:i+BLOCK_SIZE])
	for i, c in enumerate(ciphers[1:]):
		preIV = ciphers[i]
		KnownP += get_nextBlock_decrypt(c, preIV)
		print(2)
	return unpadding_pkcs7(KnownP)


cipher = open("Encrypted.txt","r").read()
print("len : %d " % len(cipher))

if check_pad(cipher) == "1":
	print("OK")
plain = OraclePaddingAttack(cipher)
print(plain)
	

