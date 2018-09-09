#!/usr/bin/env python
from pwn import *

def pow_hash(challenge, solution):
    return hashlib.sha256(challenge.encode('ascii') + struct.pack('<Q', solution)).hexdigest()

def check_pow(challenge, n, solution):
    h = pow_hash(challenge, solution)
    return (int(h, 16) % (2**n)) == 0

def solve_pow(challenge, n):
    candidate = 0
    while True:
        if check_pow(challenge, n, candidate):
            return candidate
        candidate += 1

conn = remote('17470319.quals2018.oooverflow.io', 31337)

print(conn.recvline('Challange: ')),
Challange = conn.recvline()[11:].strip()
print(Challange)

print(conn.recvuntil("n: ")),
n=conn.recvline().strip()
print(n)

challenge = Challange
n = int(n)
print('Solving challenge: "{}", n: {}'.format(challenge, n))

solution = solve_pow(challenge, n)
print(conn.recvuntil("Solution:")),
print(solution)

conn.sendline(str(solution))

## adam


print(conn.recvuntil(">"))
conn.sendline("yes")

print(conn.recvuntil("?")),
print("?")
conn.sendline("yes")

print(conn.recvuntil("?")),
print("?")

for i in range(0,8):
	conn.sendline(str(8))

print(conn.recvuntil("words")),
print(conn.recvline())
	
data = conn.recvall()
f = open("recv_fake.mp4", 'w')
f.write(data)
f.close()

#conn.interactive()