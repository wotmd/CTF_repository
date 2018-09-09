import os

PATH = "Documents/"

file_list = os.listdir(PATH)

def decode(file):
	f = open(file, 'r')
	data = f.read()
	f.close()

	f = open(file, 'w')
	data = "{:02x}".format(int(data)).decode("hex")
	f.write(data)
	f.close()
	

def decode_Recursion(filepath):
	file_list = os.listdir(filepath)
	for file in file_list:
		if os.path.isfile(filepath+file):
			original_file = file
			if file.isdigit():
				original_file = "{:02x}".format(int(file)).decode("hex")
				cmd = "mv "+filepath+file+' "'+filepath+original_file+'"'
				os.system(cmd)
			if file != original_file:
				file = original_file
				decode(filepath+file)
		else:
			if file.isdigit():
				original_file = "{:02x}".format(int(file)).decode("hex")
				cmd = "mv "+filepath+file+' "'+filepath+original_file+'"'
				os.system(cmd)
			file = original_file
			decode_Recursion(filepath+file+"/")

"""
for file in file_list:
	if file.isdigit():
		original_file = "{:02x}".format(int(file)).decode("hex")
		cmd = "mv "+PATH+file+" "+PATH+original_file
		os.system(cmd)
"""
print(file_list)
decode_Recursion(PATH)
