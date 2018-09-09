import os

def file_read(f):
	data = open(f)
	lines = [num for num in data.read().split()]
	
	return lines
	

path_dir = 'tmp'
file_list = os.listdir(path_dir)

print(file_list)

for filename in file_list:
	File = "tmp/"+filename

	line_del = file_read(File)
	prev=4
	next=5
	PASS=False
	for i,l in enumerate(line_del):
		if l[0]=='x':
			next=int(l[1:])
		else:
			next=int(l)
		if not(next==(prev+1)):
			l='*'
			line_del=line_del[0:i]
			break
		else:
			prev=next
	COMMAND = "cat /dev/null > tmp/"+filename
	print(COMMAND)
	os.system(COMMAND)
	for l in line_del:
		if(l=='*'):
			print("end")
			break
		COMMAND = "echo '"+ str(l) +" '" + ">> tmp/"+filename
		print(COMMAND)
		os.system(COMMAND)

	
