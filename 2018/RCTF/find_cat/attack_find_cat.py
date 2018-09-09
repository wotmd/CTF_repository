#!/usr/bin/env python
from subprocess import Popen, PIPE
import sys
import os

# Step1. File list set
#command = "sudo docker run -it --rm --network none -v /tmp/yourCatFood:/app/food:ro rctf_cats bash -c 'timeout 5 diff -Z <(cat food) <(find / -perm -0111 -type f)'"
#command = "sudo docker run -it --rm --network none -v /tmp/yourCatFood:/app/food:ro rctf_cats bash -c 'timeout 5 diff -Z <(cat food) <(find / -type l)'"
#1
command = "sudo docker run -it --rm --network none -v /tmp/yourCatFood:/app/food:ro rctf_cats bash -c 'timeout 5 diff -Z <(cat food) <(ls /usr/sbin)'"
#2
command = "sudo docker run -it --rm --network none -v /tmp/yourCatFood:/app/food:ro rctf_cats bash -c 'timeout 5 diff -Z <(cat food) <(ls /usr/bin)'"
#3
command = "sudo docker run -it --rm --network none -v /tmp/yourCatFood:/app/food:ro rctf_cats bash -c 'timeout 5 diff -Z <(cat food) <(ls /bin)'"
#4
command = "sudo docker run -it --rm --network none -v /tmp/yourCatFood:/app/food:ro rctf_cats bash -c 'timeout 5 diff -Z <(cat food) <(ls /sbin)'"
#5
command = "sudo docker run -it --rm --network none -v /tmp/yourCatFood:/app/food:ro rctf_cats bash -c 'timeout 5 diff -Z <(cat food) <(find /usr/bin -type l)'"
#5
command = "sudo docker run -it --rm --network none -v /tmp/yourCatFood:/app/food:ro rctf_cats bash -c 'timeout 5 diff -Z <(cat food) <(find / -perm -0001 -type l)'"



popen = Popen(command, shell=True, stdout=PIPE)
output, error = popen.communicate()

filelist = output.split("\r\n> ")
#filelist = filelist[10:]
filelist[-1]=filelist[-1][:-2]

print(len(filelist))
#exit()

for i, file in enumerate(filelist):
	command = "sudo docker run -it --rm --network none -v /tmp/yourCatFood:/app/food:ro rctf_cats bash -c 'timeout 5 diff -Z <(cat food) <("+file+" food)'"
	popen = Popen(command, shell=True, stdout=PIPE)
	output, error = popen.communicate()

	result = output.split("\n")
	cnt = 0
	
	for isCat in result:
		if "cat" in isCat:
			cnt+=1
	if(cnt >= 2):
		print("find cat??? : "+file)
		print(result)
		print(file)
		os.system("echo '"+file+"' >> catfilelist_4")
		continue
	else:
		print("%03d : Wrong.." % i)

	cnt = 0
	for isCat in result:
		if "Is a directory" in isCat:
			cnt+=1
	if(cnt >= 2):
		print("find cat??? : "+file)
		print(result)
		print(file)
		os.system("echo '"+file+"' >> catfilelist_4")
	else:
		print("%03d : Wrong.." % i)
