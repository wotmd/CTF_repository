#!/usr/bin/env python
from pwn import *
import binascii
import string
import sys
import os
from subprocess import Popen, PIPE

conn = remote('macsh.chal.pwning.xxx', 64791)

BLOCK_A = "tag "+"A"*124
BLOCK_A = BLOCK_A*128

pwd ="/home/macsh"
flag = "flag.txt"

BLOCK_COMMAND=["pwd","ls /home/macsh", "cat flag.txt"]

for BLOCK_B in BLOCK_COMMAND:
	PAD = "A"*len(BLOCK_B)
	##########  step.1
	print(conn.recvuntil('|$|>'))
	l="asdf<|>tag "+BLOCK_A+BLOCK_B
	conn.sendline(l)

	x1 = conn.recvline().strip()
	#print(x1)
	##########  step.2
	print(conn.recvuntil('|$|>'))
	l="asdf<|>tag "+PAD
	conn.sendline(l)

	x2 = conn.recvline().strip()
	#print(x2)
	##########  step.3
	print(conn.recvuntil('|$|>'))
	l="asdf<|>tag "+BLOCK_A+PAD
	conn.sendline(l)

	x3=conn.recvline().strip()
	command = "python3 xor.py "+x1+" "+x2+" "+x3
	popen = Popen(command, shell=True, stdout=PIPE)
	output, error = popen.communicate()

	output=output.strip()
	l=output+"<|>"+BLOCK_B
	print(l)
	conn.sendline(l)
	print(conn.recvline())

conn.interactive()