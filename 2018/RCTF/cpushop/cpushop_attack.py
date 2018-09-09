#!/usr/bin/env python
 
from pwn import *
import string
from subprocess import Popen, PIPE

#context.log_level = 'debug' 
#conn = remote('cpushop.2018.teamrois.cn', 43000)
conn = process(['python', 'cpushop/cpushop.py'])
 
def OrderItemFlag(id=9):
    conn.sendline("2")
    conn.recvuntil("Product ID:")
    conn.sendline(str(id))
    
    conn.recvline()
    payment=conn.recvline().strip()
    return payment
 
    
def SHA256_Extender(paym, sign, keylen):
    fake_price = "&price=1"
    keylen = str(keylen)
    
    command = './hash_extender --data "'+ paym +'" --secret '+keylen+' --append "'+ fake_price +'" --signature '+sign+' --format sha256'    
    popen = Popen(command, shell=True, stdout=PIPE)
    output, error = popen.communicate()
    
    New_signature, expanded_payment = output.split("New string: ")
    New_signature = "&sign="+(New_signature.split("New signature: "))[1].strip()
    expanded_payment = expanded_payment.strip().decode("hex")
    
    expanded_payment += New_signature
    return expanded_payment
    
def PayItem(payment):
    conn.sendline("3")
    conn.recvuntil("Your order:")
    conn.sendline(payment)
    conn.recvline()
    result=conn.recvline()
    return result
 
 
print(conn.recvuntil('Command:'))    
payment = OrderItemFlag()
 
paym, sign = payment.split("&sign=")
 
for keylen in range(8,32):
    print("keylen : " + str(keylen))
    conn.recvuntil('Command:')
    payment = SHA256_Extender(paym,sign,keylen)
    result = PayItem(payment)
    
    if "Invalid Order!" not in result:
        print(result)
        conn.interactive()
 
#conn.shutdown()  # Ctrl+D
conn.interactive()
 
"""
https://github.com/iagox86/hash_extender
./hash_extender --data "product=Intel Core i9-7900X&price=999&timestamp=1526710428630790" --secret 20 --append append --signature a3f3282990039a1cb6816c172b9e5d44308213c25d0c76d3d5dddfb627b2a0f8  --format sha256
"""
 