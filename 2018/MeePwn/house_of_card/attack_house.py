#!/usr/bin/env python
from pwn import *
import string

libc = ELF('libc.so')

env = {'LD_PRELOAD' : libc.path}
conn = process("./house_of_card", env = {'LD_PRELOAD' : libc.path})

conn.interactive()


