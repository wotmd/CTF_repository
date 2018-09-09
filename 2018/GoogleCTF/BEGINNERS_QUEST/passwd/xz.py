#!/usr/bin/env python
import os
import sys

filename = "password_xz.xz"

for i in range(0,100):
	os.system("xz -d "+filename)
	os.system("mv "+filename[:-3]+" "+filename)
	print(filename)