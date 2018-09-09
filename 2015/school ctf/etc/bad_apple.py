#!/usr/bin/env python3
import sys, binascii
from Crypto.Hash import SHA256

key = open('key.bin', 'rb').read()

message = sys.stdin.buffer.read(0x100)
if len(message) < SHA256.digest_size:
  print('len')
  exit(0)

tag, message = message[:SHA256.digest_size], message[SHA256.digest_size:]

if SHA256.new(key + message).digest() != tag:
  print('bad')
  exit(0)

if b'hello pls' in message:
  print('hello')
if b'flag pls' in message:
  print(open('flag.txt', 'r').read())

