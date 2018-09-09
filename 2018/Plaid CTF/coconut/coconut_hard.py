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

	
def AddLine_File(File, l, Bol=True):
	if(Bol==True):
		COMMAND = "echo '"+ str(l) +" '" + " >> "+File
	else:
		COMMAND = "echo 'x"+ str(l) +" '" + " >> "+File
	print(COMMAND)
	os.system(COMMAND)	
	
def Level1():
	global HALF_SUCCESS
	global WRONG
	global SUCCESS

	global IS_SUCCESS
	global File
	global LV
	global conn
	LV=1
	#STEP1
	while(True):
		if not IS_SUCCESS:
			conn = remote('coconut.chal.pwning.xxx', 6817)
		print(conn.recvuntil('Testing '))
		Testing = conn.recvuntil(', threshold').strip()
		Testing = Testing[:-11]

		print(Testing)
		File = "tmp/"+Testing
		
		conn.recvuntil("delete can only")
		MIN = conn.recvuntil("and")
		print(MIN)
		MIN = parseint(MIN)
		
		MAX = conn.recvline()
		print(MAX)
		MAX = parseint(MAX)		
		
		if (os.path.exists(File)==False) or (MIN>=6):
			print("STEP 2")
			#conn.interactive()
			return (MIN,MAX)
		
		##file exists
		line_del = [str(MIN)]
		
		if(os.path.exists(File)):
			line_del = file_read(File)
		for l in line_del:
			if not (l[0]=='x'):
				#print(l)
				conn.sendline(l)
			#else:
			#	print(l)
		if(os.path.exists(File)):
			if not (line_del[-1][0]=='x'):
				end_del = int(line_del[-1])+1
			else:
				end_del = int(line_del[-1][1:])+1
			if(end_del<=MAX):
				print("end_rm_line : "+str(end_del))
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
			AddLine_File("tmp/"+Testing, end_del)
			conn.close()
			LV=1
		elif WRONG in is_all_right:
			AddLine_File("tmp/"+Testing, end_del,False)
			conn.close()
			LV=1
		elif SUCCESS in is_all_right:
			print("yes")
			print("LEVEL : "+str(LV))
			LV=LV+1
			IS_SUCCESS = True
		else:
			conn.recvline()
			conn.recvline()
			
def QuickSearch(min, max):
	if(min==max):
		print("equal!")
		return [str(min),str(max)]
	mid = (min+max)//2
	left = str(min)+"-"+str(mid)
	right = str(mid+1)+"-"+str(max)
	return [left,right]

	
def changeGoodLine(File, change_line):
	line_del = file_read(File)
	## DB_reset
	COMMAND = "cat /dev/null > "+File
	print(COMMAND)
	os.system(COMMAND)
	
	for l in line_del:
		if l==change_line:
			AddLine_File(File,l[2:])
		else:
			AddLine_File(File,l)
			
def changeSplitLine(File, change_line):
	line_del = file_read(File)
	## DB_reset
	COMMAND = "cat /dev/null > "+File
	print(COMMAND)
	os.system(COMMAND)
	
	for l in line_del:
		if l==change_line:
			left, right = l.strip('x').split('-')
			left=int(left)
			right=int(right)
			left,right = QuickSearch(left,right)
			if(left==right):
				AddLine_File(File,left,False)
			else:
				AddLine_File(File,"x"+left,False)
				AddLine_File(File,"x"+right,False)
		else:
			AddLine_File(File,l)
			
		
def Level2(MIN,MAX):
	global HALF_SUCCESS
	global WRONG
	global SUCCESS

	global IS_SUCCESS
	global File
	global LV
	global conn

	IS_SUCCESS = True

	#STEP 2
	while(True):	
		##file no exists line_delete
		line_del = ["xx"+str(MIN)+"-"+str(MAX)]
		revive=line_del[0]
		##file exists read line_DB
		if(os.path.exists(File)):
			line_del = file_read(File)
		else:
			AddLine_File(File,revive)
		
		for l in line_del:
			if not (l[0]=='x'):
				print(l)
				end_del = l
				conn.sendline(l)
		if(os.path.exists(File)):
			revive="None"
			for l in line_del:
				if (l[0:2]=='xx'):
					revive = l
					break
			if not(revive=="None"):
				conn.sendline(revive[2:])
			else: # QuickSearch
				conn.interactive()
			"""
				revive=l[1:]
				left, right = revive.split('-')
				left=int(left)
				right=int(right)
				left,right = QuickSearch(left,right)
				if(left==right):
					revive=left
					conn.sendline(left)
				else:
					conn.sendline(left)
					revive = "xx"+right
					#right xx save"""
		conn.sendline("#")
		
		#conn.recvuntil("Result:")
		print(conn.recvline())
		print(conn.recvline())
		print(conn.recvline())
		is_all_right = conn.recvline()
		print(is_all_right)
		IS_SUCCESS = False
		
		if HALF_SUCCESS in is_all_right:
			changeGoodLine(File,revive)
			conn.close()
		elif WRONG in is_all_right:
			changeSplitLine(File,revive)
			conn.close()

		elif SUCCESS in is_all_right:
			print("yes")
			print("LEVEL : "+str(LV))
			LV=LV+1
			IS_SUCCESS = True
			#print(conn.recvuntil("}"))
			#conn.interactive()
		else:
			conn.recvline()
			conn.recvline()

		if not IS_SUCCESS:
			break
			#conn = remote('coconut.chal.pwning.xxx', 6817)
		print(conn.recvuntil('Testing '))
		Testing = conn.recvuntil(', threshold').strip()
		Testing = Testing[:-11]

		print(Testing)
		File = "tmp/"+Testing
		"""
		if not (os.path.exists(File)):
			print(conn.recvuntil("Note:"))
			conn.interactive()
		"""
		conn.recvuntil("delete can only")
		MIN = conn.recvuntil("and")
		print(MIN)
		MIN = parseint(MIN)
		
		MAX = conn.recvline()
		print(MAX)
		MAX = parseint(MAX)
		

HALF_SUCCESS = "Correct but didn't meet threshold!"
WRONG = "Wrong Result!"
SUCCESS = "Success!"

IS_SUCCESS = True
File=""
LV = 1
conn = remote('coconut.chal.pwning.xxx', 6817)
while(True):
	min,max=Level1()
	Level2(min,max)

"""

COMMAND = "echo '"+ "5" +" '" + ">> tmp/"+Testing
print(COMMAND)

os.system("ls")
os.system(COMMAND)
conn.close()



X = 5 6
	
7-10 #

"""