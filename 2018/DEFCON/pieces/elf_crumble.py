from itertools import permutations
from subprocess import Popen, PIPE
import os
import sys

Connect=[]
for i in range(8):
	Connect.append("fragment_"+str(i+1)+".dat")
print(Connect)

for c in permutations(Connect,8):
	i=i+1
	print("%d attack" % i)
	
	command="cat head > tmp"
	os.system(command)
	for order in c:
		command="cat "+order+" >> tmp";
		os.system(command)
	command="cat tail >> tmp"
	os.system(command)
	
	command="chmod +x tmp"
	os.system(command)
	
	command = "./tmp"
	popen = Popen(command, shell=True, stdout=PIPE)
	output, error = popen.communicate()
	
	command="echo '"+str(output)+"' >> output"
	os.system(command)
	print(output)

	
	
