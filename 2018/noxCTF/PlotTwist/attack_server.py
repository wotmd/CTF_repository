#!/usr/bin/env python
from pwn import *
import string
from randcrack import RandCrack
#https://github.com/tna0y/Python-random-module-cracker


conn = remote("chal.noxale.com", 5115)

def get_key(rc):
	conn.recvuntil("Please insert the decryption key:\n")
	conn.send("0"*16*624)
		
	for i in range(624):
		conn.recvuntil("Wrong! The key was: ")
		key = conn.recv(16)
		rc.submit(int(key))
		conn.recvuntil("Please insert the decryption key:\n")

	key = str(rc.predict_getrandbits(32)).rjust(16, '0')
	return key

rc = RandCrack()
key = get_key(rc)
conn.send(key)

conn.interactive()


