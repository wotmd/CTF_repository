#!/usr/bin/env python2
import os

SBITS = 8
PBITS = 64

key = open('key.bin', 'rb').read()
assert len(key) == 8

################################################################################

R = 4

S = [74, 82, 142, 45, 149, 197, 166, 19, 182, 108, 201, 155, 136, 218, 247, 135, 194, 79, 189, 239, 252, 174, 131, 209, 116, 38, 11, 59, 0, 24, 53, 103, 249, 171, 134, 212, 199, 62, 184, 234, 144, 161, 48, 96, 113, 35, 14, 92, 89, 105, 68, 22, 75, 117, 122, 40, 183, 18, 242, 160, 179, 225, 204, 158, 73, 43, 6, 84, 71, 86, 56, 106, 207, 157, 176, 226, 125, 163, 172, 12, 187, 233, 195, 150, 133, 215, 250, 168, 5, 95, 114, 32, 51, 97, 76, 30, 237, 210, 27, 173, 190, 148, 193, 147, 54, 100, 121, 255, 8, 90, 119, 37, 66, 16, 61, 111, 196, 46, 3, 81, 244, 65, 139, 217, 202, 152, 181, 231, 44, 126, 128, 1, 223, 64, 109, 98, 154, 200, 229, 141, 164, 246, 219, 137, 238, 47, 145, 124, 208, 130, 175, 253, 88, 10, 39, 87, 102, 52, 25, 13, 213, 165, 170, 248, 235, 185, 236, 198, 99, 49, 28, 78, 93, 41, 34, 112, 23, 69, 104, 58, 221, 123, 21, 4, 29, 243, 222, 140, 159, 205, 110, 178, 85, 7, 42, 120, 107, 57, 20, 70, 227, 177, 156, 206, 138, 143, 162, 240, 151, 228, 232, 186, 169, 251, 214, 132, 33, 115, 94, 220, 31, 77, 63, 50, 127, 254, 211, 129, 146, 192, 83, 191, 26, 72, 101, 55, 36, 118, 91, 9, 224, 60, 17, 67, 80, 2, 188, 241, 216, 15, 167, 245, 230, 180, 153, 203]

P = [57, 55, 30, 48, 26, 47, 17, 29, 24, 13, 53, 37, 34, 35, 0, 8, 61, 28, 39, 51, 56, 62, 52, 36, 33, 46, 38, 25, 32, 44, 45, 5, 15, 23, 7, 58, 6, 4, 49, 2, 3, 19, 31, 60, 59, 1, 42, 12, 50, 40, 18, 43, 21, 16, 27, 54, 11, 20, 63, 41, 14, 10, 22, 9]

invS = map(lambda i: i[1], sorted([S[i], i] for i in range(1 << SBITS)))
invP = map(lambda i: i[1], sorted([P[i], i] for i in range(PBITS)))

assert list(sorted(S)) == range(1 << SBITS)
assert list(sorted(P)) == range(PBITS)

################################################################################

def xor(xs, ys):
  return ''.join(chr(ord(x) ^ ord(y)) for x, y in zip(xs, ys))

def permute_bits(p, x):
  y = ''.join(map(lambda i: bin(ord(i))[2:].zfill(8), x)).zfill(PBITS)
  x = [None] * PBITS
  for i, j in zip(range(PBITS), p):
    x[j] = y[i]
  x = ''.join(x)
  x = [x[i:i+8] for i in range(0, len(x), 8)]
  x = ''.join(map(lambda i: chr(int(i, 2)), x))
  return x

################################################################################

def E(k, x):
  for r in range(R):
    x = ''.join(map(lambda i: chr(S[ord(i)]), x))
    if r < R - 1:
      x = permute_bits(P, x)
    x = xor(k, x)
    k = k[1:] + k[:1]
  return x

################################################################################

def D(k, x):
  ks = [k[i%8:] + k[:i%8] for i in range(R)]
  for r, k in reversed(zip(range(R), ks)):
    x = xor(k, x)
    if r < R - 1:
      x = permute_bits(invP, x)
    x = ''.join(map(lambda i: chr(invS[ord(i)]), x))
  return x

################################################################################

def EE(k, message):
  blocks = [message[i : i + PBITS // 8] for i in range(0, len(message), PBITS // 8)]
  if len(blocks[-1]) == PBITS // 8:
    blocks.append(chr(PBITS // 8) * PBITS // 8)
  else:
    n = PBITS // 8 - len(blocks[-1])
    blocks = blocks[:-1] + [blocks[-1] + chr(n) * n]
  prev_block = os.urandom(PBITS // 8) #IV
  message = prev_block
  for block in blocks:
    block = E(k, ''.join(chr(ord(x) ^ ord(y)) for x, y in zip(block, prev_block)))
    message += block
    prev_block = block
  return message

def DD(k, message):
  blocks = [message[i : i + PBITS // 8] for i in range(0, len(message), PBITS // 8)]
  prev_block = blocks[0]
  blocks = blocks[1:]
  message = ''
  for block in blocks:
    message += ''.join(chr(ord(x) ^ ord(y)) for x, y in zip(D(k, block), prev_block))
    prev_block = block
  n = ord(message[-1])
  message = message[:-n]
  return message

f = open('stuff.txt', 'w')

d = EE(key, open('flag.txt', 'rb').read().strip())
print d.encode('hex')
f.write('%s\n' % d.encode('hex'))
p = DD(key, d)
print p

for i in range(256):
  p = os.urandom(8)
  c = E(key, p)
  f.write('%s %s\n' % (p.encode('hex'), c.encode('hex')))

f.close()

