#from itertools import permutations
from pwn import *
import os

want= "be >=5 and <=15:"
want2= "be >=5 and <=17:"

while(True):
	conn = remote('coconut.chal.pwning.xxx', 6817)
	print(conn.recvuntil('delete can only'))
	the_random = conn.recvline()

	print(the_random)

	if want in the_random:
		conn.sendline("7-10")
		conn.sendline("#")
		print(conn.recvuntil('delete can only'))
		the_random = conn.recvline()
		if want2 in the_random:
			conn.interactive()
	else:
		conn.close()

os.sys("tmp/")



"""
X = 5 6
	
7-10 #

"""