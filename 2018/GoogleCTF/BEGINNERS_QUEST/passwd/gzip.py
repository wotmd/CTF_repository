#!/usr/bin/env python
import os
import sys

filename = "password_gzip.gz"

for i in range(0,10):
	os.system("gzip -d "+filename)
	os.system("mv "+filename[:-3]+" "+filename)
	print(filename)