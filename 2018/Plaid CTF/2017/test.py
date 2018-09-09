#!/usr/bin/env python
from pwn import *
import binascii
import hashlib
import os
import signal
#import socketserver
import string
import sys
import itertools

N = 128
OUTPUT = 32
HIDDEN = N-OUTPUT
TIME = 120
 
alpha = [chr(i) for i in range(0x20, 0x7F + 1)]
 
conn = remote('lcg.chal.pwning.xxx', 6051)
#conn = process('python3 lcg.py')
print(conn.recvuntil('with'))
prefix = conn.recvuntil('of').strip()
prefix = prefix[:-3]
print("prefix : " + prefix)
print("len : " + str(len(prefix)))

word = prefix
for cand in itertools.product(alpha, repeat=6):
	#print(cand)
	cand_word = prefix + ''.join(cand)
	cand_word = cand_word.encode('utf8')
	digest = hashlib.sha256(cand_word).hexdigest()
	#print(digest)
	if digest[-6:] == 'ffffff': # and ord(digest[3]) >= 0xF0:
		word = cand_word
		break
l=prefix+word
l=l.encode('utf8')
l=word.encode('utf8')
print(hashlib.sha256(l).hexdigest()[-6:])

conn.sendline(l)

print(conn.recvline())
print(conn.recvline())
print(conn.recvline())
conn.interactive()













