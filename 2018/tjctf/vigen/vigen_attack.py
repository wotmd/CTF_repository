#!/usr/bin/env python
from itertools import permutations
import hashlib
import string

# Alphabet used as reference (M)
# ABCDEFGHIJKLMNOPQRSTUVWXYZ
source = string.ascii_uppercase

# Key alphabet (K) shifted 1 position to the left
# BCDEFGHIJKLMNOPQRSTUVWXYZA
shift = 1
matrix = [ source[(i + shift) % 26] for i in range(len(source)) ]

def decoder(thistext, mykey):
	control = 0
	plaintext = []

	for x,i in enumerate(thistext.upper()):
	    if i not in source: 
	        #If the symbol is not in our reference alphabet, we simply print it
	        plaintext.append(i)
	        continue
	    else:
	        #Wrap around the mykey string 
	        control = 0 if control % len(mykey) == 0 else control 
	        #Calculate the position M[i] = (C[i]-K[i]) mod len(M)
	        result = (matrix.index(i) - matrix.index(mykey[control])) % 26
	        #Add the symbol in position "result" to be printed later
	        plaintext.append(source[result])
        	control += 1
	plain = ""
	for p in plaintext:
		plain += p
	return plain

hash = "8304c5fa4186bbce7ac030d068fdd485040e65bf824ee70b0bdbac03862bec93"

ciphertext = "uucbx{simbjyaqyvzbzfdatshktkbde}"

cand = "BLAIS"



for c in permutations(source,4):
	candi = cand
	for t in c:
		candi += t
	plaintext = decoder(ciphertext, candi).lower()

	digest = hashlib.sha256(plaintext).hexdigest()
	if digest == hash : 
		print(candi)

print(digest)






