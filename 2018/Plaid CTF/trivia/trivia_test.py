#!/usr/bin/env python3
import binascii
import collections
import hashlib
import random
import os
import string
import sys


def bytestobits(b):
    return [(byte >> (7-i)) & 1 for byte in b for i in range(8)]

def bitstobytes(b):
    return bytes([sum(b[i+j] << (7-j) for j in range(8)) for i in range(0, len(b), 8)])

def trivium(key, iv, numbytes):
    assert(len(key) == 10)
    assert(len(iv) == 10)

    init_list = bytestobits(key)
    init_list += [0]*13

    init_list += bytestobits(iv)
    init_list += [0]*4

    init_list += [0]*108
    init_list += [1, 1, 1]
    state = collections.deque(init_list)

    def genbit():
        t_1 = state[65]  ^ state[92]
        t_2 = state[161] ^ state[176]
        t_3 = state[242] ^ state[287]

        out = t_1 ^ t_2 ^ t_3

        s_1 = t_1 ^ state[90]  & state[91]  ^ state[170]
        s_2 = t_2 ^ state[174] & state[175] ^ state[263]
        s_3 = t_3 ^ state[285] & state[286] ^ state[68]

        state.rotate(1)

        state[0] = s_3
        state[93] = s_1
        state[177] = s_2

        return out
    print(state)
    # warmup
    for i in range(576):
        genbit()
    print(state)
    # generate keystream
    stream = [genbit() for i in range(8*numbytes)]

    return bitstobytes(stream)

def test():
    l = [0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1]
    b = b'\x12\x34\x56\x78'
    assert bytestobits(bitstobytes(l)) == l
    assert bitstobytes(bytestobits(b)) == b
    assert bytestobits(b'\xf0') == [1, 1, 1, 1, 0, 0, 0, 0]

test()

def myrecv(self, n):
	x = request.recv(n)
	if n > 0 and x == b'':
		sys.exit(1)
	return x

def recvline(self, limit):
	s = b""
	while not s.endswith(b"\n") and len(s) <= limit:
		s += myrecv(1)
	return s


# the good stuff

key = os.urandom(10)
print(key)
print("".join('{:02x}'.format(x) for x in key))

tmp = bytestobits(key)
print(tmp[:65])
print(tmp[65:])

print("Commands:\n    keystream [iv] [number of bytes]\n    guess [key]\n")
for i in range(5000):
	l = input().strip().split()#recvline(48).strip().split() ##recvline(48).strip().split()
	print(l)
	if l[0] == "keystream":
		print("len :" + str(len(l[1])))
		iv = binascii.unhexlify(l[1])
		numbytes = int(l[2])
		print("numbytes" + str(numbytes))
		print("len :" + str(len(iv)))
		if 1 <= numbytes <= 16 and len(iv) == 10:
			stream = trivium(key, iv, numbytes)
			print(binascii.hexlify(stream)+b"\n")
			tmp = bytestobits(binascii.hexlify(stream))
			print(tmp)
			tmp.reverse()
			print(tmp)
		else:
			print("Invalid format.\n")
	elif l[0] == "guess":
		print(len(l))
		if len(l) == 2 and binascii.unhexlify(l[1]) == key:
			print("Congrats!")
		else:
			print("Nope.\n")
		exit()
	else:
		print(b"Invalid command!\n")