#!/usr/bin/env python3
import binascii
import hashlib
import os
import signal
import string
import sys


N = 128
assert N % 8 == 0
OUTPUT = 32
HIDDEN = N-OUTPUT
TIME = 120

def gcd(u, v):
    while v:
        u, v = v, u % v
    return abs(u)
	
def nextstate(state, mult, inc, modulus):
    return (state*mult + inc) % modulus




# proof of work
MODULUS = int(binascii.hexlify(os.urandom(N // 8)), 16)
MULT = 0
INC = 0
STATE = 0

while not (1 <= MULT < MODULUS and gcd(MULT, MODULUS) == 1):
	MULT = int(binascii.hexlify(os.urandom(N // 8)), 16)
while not (1 <= INC < MODULUS and gcd(INC, MODULUS) == 1):
	INC = int(binascii.hexlify(os.urandom(N // 8)), 16)
while not (1 <= STATE < MODULUS):
	STATE = int(binascii.hexlify(os.urandom(N // 8)), 16)

print(MODULUS)
print(MULT)
print(INC)
print(STATE)	
	
	
# outputs
s = b""
for i in range(40):
	output = STATE >> HIDDEN
	s += str(output).encode("utf8") + b" "
	STATE = nextstate(STATE, MULT, INC, MODULUS)
print(b"Outputs: " + s + b"\n")

signal.alarm(TIME)

# predict
failures = 0
for i in range(200):
	l = int(input())
	output = STATE >> HIDDEN
	print(STATE)
	print(output)
	if output != l:
		print("Nope. (Expected {}.)\n".format(output).encode('utf8'))
		failures += 1
		if failures >= 5:
			print(b"Too many failures. Better luck next time!\n")
			exit()
	else:
		print(b"Good.\n")
	STATE = nextstate(STATE, MULT, INC, MODULUS)

print("Congrats! ")
