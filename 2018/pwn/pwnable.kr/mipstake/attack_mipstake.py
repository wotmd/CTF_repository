from pwn import *
from echo1flag import passwd
local = False

if local:
	conn = process(['gdb-peda',"./mipstake"])
	conn.sendline("break system")
	conn.sendline("r")
	#conn = process("./mipstake")
else:
	s = ssh(user='mipstake',host='pwnable.kr',port=2222,password=passwd)
	conn = s.connect_remote('localhost', 9033)

conn.interactive()
