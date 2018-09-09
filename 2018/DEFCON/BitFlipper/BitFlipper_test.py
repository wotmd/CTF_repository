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

conn = remote('61421a06.quals2018.oooverflow.io', 5566)

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

## baby pwn

conn.interactive()