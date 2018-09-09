import os
import string
from subprocess import Popen, PIPE

path = "/home/sherlock/workstation/crytoTool/JohnTheRipper/run/"

password_list=""
def john(zip):
	global password_list
	cmd = "/home/sherlock/workstation/crytoTool/JohnTheRipper/run/zip2john "
	cmd += zip
	cmd += " > zip.hash"
	os.system(cmd)
	
	cmd = "/home/sherlock/workstation/crytoTool/JohnTheRipper/run/john zip.hash"
	
	popen = Popen(cmd, shell=True, stdout=PIPE)
	output, error = popen.communicate()
	#print(output)
	
	password = (output.split("\n")[1]).split("(")[0].strip()
	print(password)
	password_list += ", "+password
	cmd = "rm /home/sherlock/workstation/crytoTool/JohnTheRipper/run/john.pot"
	os.system(cmd)
	return password
	
#ilovehim
cmd = "unzip -P "
password = "brandon1"

for i in range(499,237,-1):
	zip = str(i)+".zip"
	password = john(zip)
	os.system(cmd+password+" "+zip)
	#exit(1)
print(password_list)
