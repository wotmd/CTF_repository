#!/usr/bin/env python
from pwn import *
import binascii
import hashlib
import os
import signal
import string
import sys
import itertools


conn = remote('trivial.chal.pwning.xxx', 5419)
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













