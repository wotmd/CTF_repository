#!/usr/bin/python3

import sys
import os

def encrypt(message, key):
    message = list(message)
    key = list(key)
    for i, kb in enumerate(key):
        step = (kb % len(key)) + 1
        for j in range(i, len(message), step):
            message[j] ^= kb
    return bytes(message)
	
with open(sys.argv[2], "wb") as f:
    f.write(encrypt(open(sys.argv[1], 'rb').read(), os.urandom(16)))