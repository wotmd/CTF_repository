import string

def strxor(a,b): #xor two string of different lengths
	if len(a)>len(b):
		return "".join([chr(ord(x)^ord(y)) for (x,y)in zip(a[:len(b)],b)])
	else :
		return "".join([chr(ord(x)^ord(y)) for (x,y)in zip(a,b[:len(a)])])
		
		
#example

m1="sherlock"
m2="keylock"
m3=strxor(m1,m2)
print m3