import os
import sys
import string

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
#os.system(COMMAND)	


path1 = "tmp"
path2 = "test"

file1_list = os.listdir(path1)
file2_list = os.listdir(path2)

if(file1_list==file2_list):
	print(True)
else:
	for i in range(len(file1_list)):
		if not(file1_list[i]==file2_list[i]):
			COMMAND = "cp "+ path2 +"/" +file2_list[i]+" "+path1+"/"
			print(COMMAND)
			os.system(COMMAND)
			break
	print(path1+"_len : "+str(len(file1_list)))
	print(path2+"_len : "+str(len(file2_list)))
	print("exit")
	exit()
	
for i in range(len(file1_list)):
	l1=len(file_read(path1+"/"+file1_list[i]))
	l2=len(file_read(path2+"/"+file2_list[i]))
	
	if(l1<l2):
		COMMAND = "cp "+ path2 +"/" +file2_list[i]+" "+path1+"/"
		print(COMMAND)
		os.system(COMMAND)


