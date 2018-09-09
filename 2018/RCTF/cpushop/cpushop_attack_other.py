#!/usr/bin/env python
from pwn import *
import hashpumpy

conn = process(['python', 'cpushop/cpushop.py'])
 
def OrderItemFlag(id=9):
    conn.sendline("2")
    conn.recvuntil("Product ID:")
    conn.sendline(str(id))
    
    conn.recvline()
    payment=conn.recvline().strip()
    return payment

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
    n = hashpumpy.hashpump(sign, paym, '&price=1', keylen)
    payment = n[1]+"&sign="+n[0]
    result = PayItem(payment)
    
    if "Invalid Order!" not in result:
        print(result)
        conn.interactive()

conn.interactive()

