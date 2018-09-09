#from itertools import permutations
from pwn import *
import os
import sys
import string

def parseint(string):
    return int(''.join([x for x in string if x.isdigit()]))

def file_read(f):
	data = open(f)
	lines = [num for num in data.read().split()]
	
	return lines

HALF_SUCCESS = "Correct but didn't meet threshold!"
WRONG = "Wrong Result!"
SUCCESS = "Success!"

IS_SUCCESS = True
LEVEL=0
conn = remote('coconut.chal.pwning.xxx', 6817)
while(True):
	LEVEL=LEVEL+1
	if not IS_SUCCESS:
		conn = remote('coconut.chal.pwning.xxx', 6817)
	print(conn.recvuntil('Testing '))
	Testing = conn.recvuntil(', threshold').strip()
	Testing = Testing[:-11]

	print(Testing)
	File = "tmp/"+Testing
	
	if not (os.path.exists(File)):
		print(conn.recvuntil("Note:"))
		print(conn.recvline())
		print("LEVEL : "+str(LEVEL))
		conn.interactive()
	
	conn.recvuntil("delete can only")
	MIN = conn.recvuntil("and")
	print(MIN)
	MIN = parseint(MIN)
	
	MAX = conn.recvline()
	print(MAX)
	MAX = parseint(MAX)

	##file exists
	line_del = [str(MIN)]
	if(MIN>=6):
		conn.interactive()
	
	if(os.path.exists(File)):
		line_del = file_read(File)
	for l in line_del:
		if not (l[0]=='x'):
			print(l)
			conn.sendline(l)
		else:
			print(l)
	if(os.path.exists(File)):
		if not (line_del[-1][0]=='x'):
			end_del = int(line_del[-1])+1
		else:
			end_del = int(line_del[-1][1:])+1
		if(end_del<=MAX):
			print(str(end_del))
			conn.sendline(str(end_del))
	else:
		end_del = line_del[-1]
	conn.sendline("#")
	
	#conn.recvuntil("Result:")
	print(conn.recvline())
	print(conn.recvline())
	print(conn.recvline())
	is_all_right = conn.recvline()
	print(is_all_right)
	IS_SUCCESS = False
	if HALF_SUCCESS in is_all_right:
		COMMAND = "echo '"+ str(end_del) +" '" + ">> tmp/"+Testing
		print(COMMAND)
		os.system(COMMAND)
		conn.close()
	elif WRONG in is_all_right:
		COMMAND = "echo 'x"+ str(end_del) +" '" + ">> tmp/"+Testing
		print(COMMAND)
		os.system(COMMAND)
		conn.close()
	elif SUCCESS in is_all_right:
		print("yes")
		IS_SUCCESS = True
	else:
		conn.recvline()
		conn.recvline()
		
"""

COMMAND = "echo '"+ "5" +" '" + ">> tmp/"+Testing
print(COMMAND)

os.system("ls")
os.system(COMMAND)
conn.close()



X = 5 6
	
7-10 #

"""