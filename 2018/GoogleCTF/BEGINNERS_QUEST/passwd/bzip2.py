#!/usr/bin/env python
import os
import sys

filename = "password_bzip2.bz2"

for i in range(0,10):
	os.system("bzip2 -kd "+filename)
	os.system("mv "+filename[:-4]+" "+filename)
	print(filename)