from Crypto import Random
from Crypto.Cipher import AES
from functools import reduce
import binascii
import string
import sys
import os


N = AES.block_size


def to_int(b):
    return int(binascii.hexlify(b), 16)
def encode(cmdline):
    return cmdline.encode('utf-8')
def to_block(b):
    return bytes.fromhex('{:0{width}x}'.format(b, width=N*2))
def to_blocks(m):
    m += to_block(len(m))
    padb = N - len(m) % N
    m += bytes([padb]) * padb
    blocks = [m[N*i : N*(i+1)] for i in range(len(m) // N)]
    return blocks
def rot(n, c):
    return (n >> c) | ((n & ((1 << c) - 1)) << (8 * N - c))
def f(k0, i):
    return to_block(rot(to_int(k0), i % (8 * N)))
def xor(x, y):
    return bytes([xe ^ ye for xe,ye in zip(x,y)])


def fmac(k0, k1, m):
    C = AES.new(k1, AES.MODE_ECB)
    bs = [C.encrypt(xor(b, f(k0, i))) for i,b in enumerate(to_blocks(m))]
    print("bs")
    print(bs)
    return reduce(xor, bs, b"\x00" * N)

k0=b'\x9d\xb7X\xfb]\x89\xee\x0cL\x8f\x18#\xdf\xf4\xc4_'
k1=b'zZ\x9b\x14\x8b\xd2\xc9\xf6\x8e\xc1\xebl\xcc/$\x94'

m="tag AAAAAAAAAAAAls .////////////"
print(len(m))
print(to_blocks(encode(m)))

m="tag AAAAAAAAAAAA"
print(len(m))
print(to_blocks(encode(m)))

"""
m="\x10"*16+"\x07"*16
print("\n\nCrypt:")
print(fmac(k0, k1, encode(m)))
m="AAAAAAAAAAAAAAAA"
print("\n\nCrypt:")
print(fmac(k0, k1, encode(m)))
for i,b in enumerate(to_blocks(encode(m))):
    print(i)
    print(b)
"""

m="tag AAAAAAAAAAAAls .////////////BBBBBBBBBB"
#m="A AAAAAAAAAAAAAA"+"B"*16
#m = m*2
print("\n\nCrypt:")
print(fmac(k0, k1, encode(m)))
print("this")
for i,b in enumerate(to_blocks(encode(m))):
    print(i)
    print(b)
	
m="tag AAAAAAAAAAAABBBBBBBBBB"
#m="A AAAAAAAAAAAAAA"+"B"*16
#m = m*2
print("\n\nCrypt:")
print(fmac(k0, k1, encode(m)))
print("this")
for i,b in enumerate(to_blocks(encode(m))):
    print(i)
    print(b)
print(binascii.hexlify(k0))
s=f(k0,8)
print(binascii.hexlify(s))
print(s)
	
"""
print("xeye")
for xe,ye in zip(m,f(k0,1)):
    print(xe)
    print(ye)
   """
