#!/usr/bin/python
from os import path, listdir, chdir
import sys

chdir("/tmp")

def get_clean_path(dirty_path):
    FILTER = ['etc', 'home/', '/home', '~/', '/~', 'proc/', '/proc', 'dev/', '/dev', 'self/', '/self', './', 'passwd', 'group', 'run', 'dev', 'usr', 'var', 'opt']
    for f in FILTER:
        if input_path.find(f) != -1:
            print_custom("NO !")
            exit(-1)

    return path.expanduser(input_path)

def print_custom(str_):
    print(str_)
    sys.stdout.flush()

sys.stdout.flush()
sys.stdin.flush()
sys.stderr.flush()
print_custom("Hello Thie service is running under the AWS !!")
print_custom("flag file is in some user's home directory.")
print_custom("have fun !!")

print_custom("dir to list: ")
input_path = raw_input("")
clean_path = get_clean_path(input_path)

files = listdir(clean_path)

print_custom("List Dir")
print_custom(files)

print_custom("file to read: ")
input_path = raw_input()
clean_path = get_clean_path(input_path)

with open(clean_path, "rb") as f:
    data = f.read()
    f.close()

print_custom("Read File")
print_custom(data)

print_custom("Bye")