from pwn import *
import string



alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()_+{}.,/'"
table = [alpha[i:i+30] for i in range(0,len(alpha),30)]
print(table)

p_table = {}

for plain in table:
	conn = process("./babyre")
	conn.sendline("A"*32)
	conn.sendline(str(32))

	conn.sendline(plain)
	conn.recvuntil("try again")
	for i in range(len(plain)):
		#print(plain[i]+" :"),
		P = conn.recvline().strip().upper()
		p_table[P]=plain[i]
	conn.close()

f = open("out", 'r')
lines = f.readlines()
f.close()

flag = ""

for c in lines:
	if c[:8] in p_table:
		flag += p_table[c[:8]]
	else:
		flag += "?"
	if c[8:16] in p_table:
		flag += p_table[c[8:16]]
	else:
		flag += "?"


print(flag)

